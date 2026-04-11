# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Client-related business logic and database interactions."""

import logging

from app.database import get_supabase
from app.text_generation.service import fetch_client_generations
from datetime import datetime, timezone 
from app.config import get_r2_logos_client, R2_LOGOS_BUCKET_NAME, R2_PUBLIC_URL
from fastapi import UploadFile, HTTPException
from app.text_generation.schemas import GenerationsResponse


logger = logging.getLogger(__name__)

async def get_clients_by_user(user_id: str) -> list[dict]:
    """Return all active clients for a given user_id (soft-delete aware)."""

    db = get_supabase()

    response = (
        db.table("clients")
        .select("*")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .execute()
    )
    logger.info(f"Retrieved clients for user: {len(response.data)}")

    return response.data or []

async def get_client_by_id(client_id: int, user_id: str) -> dict | None:
    """Return a specific client by ID, if it belongs to the user and is not deleted."""

    db = get_supabase()

    try:
        response = (
            db.table("clients")
            .select("*")
            .eq("id", client_id)
            .eq("user_id", user_id)
            .is_("deleted_at", "null")
            .execute()
        )
    except Exception as exc:
        logger.error(f"Error fetching client {client_id} for user {user_id}: {exc}")
        return None

    return response.data[0] if response.data else None


async def get_client_generations(client_id: int, user_id: str) -> list[GenerationsResponse]:
    """Return generations for a specific client."""

    return await fetch_client_generations(client_id, user_id)


async def create_client(user_id: str, client_name: str, brand_voice: str | None) -> dict:
    """Insert a new client row and return the created record."""

    payload = {
        "user_id": user_id,
        "client_name": client_name,
        "brand_voice": brand_voice,
    }

    db = get_supabase()

    response = db.table("clients").insert(payload).execute()
    return response.data[0]

ALLOWED_FIELDS = {"client_name", "brand_voice", "platforms", "custom_folders", "logo_url"}

async def update_client(client_id: int, user_id: str, **fields) -> dict | None:
    safe_fields = {k: v for k, v in fields.items() if k in ALLOWED_FIELDS}
    if not safe_fields:
        return None
    
    db = get_supabase()
    response = (
        db.table("clients")
        .update(safe_fields)
        .eq("id", client_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )
    logger.info(f"Updated client {client_id} for user {user_id}")
    
    return response.data[0] if response.data else None


async def soft_delete_client(client_id: int, user_id: str) -> bool:
    """Soft-delete a client. Returns True if deleted, False if not found."""

    db = get_supabase()

    response = (
        db.table("clients")
        .update({"deleted_at": datetime.now(timezone.utc).isoformat()})
        .eq("id", client_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    return bool(response.data)

async def upload_client_logo(client_id: int, file: UploadFile, user_id: str) -> dict:
    """Upload a client logo to R2 logos bucket and update the client record."""
    
    db = get_supabase()
    
    # Verify ownership
    client = db.table("clients").select("id").eq("id", client_id).eq("user_id", user_id).single().execute()
    if not client.data:
        raise HTTPException(status_code=404, detail="Client not found")
    
    r2 = get_r2_logos_client()
    path = f"{user_id}/{client_id}/logo/{file.filename}"
    
    try:
        contents = await file.read()
        r2.put_object(
            Bucket=R2_LOGOS_BUCKET_NAME,
            Key=path,
            Body=contents,
            ContentType=file.content_type,
        )
        logger.info("Successfully uploaded logo to R2")
    except Exception as e:
        logger.error(f"Error uploading logo to R2: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload logo") from e
    
    public_url = f"{R2_PUBLIC_URL}/{path}"
    
    try:
        response = (
            db.table("clients")
            .update({"logo_url": public_url})
            .eq("id", client_id)
            .eq("user_id", user_id)
            .execute()
        )
        return {"logo_url": public_url}
    except Exception as e:
        logger.error(f"Error saving logo_url: {e}")
        raise HTTPException(status_code=500, detail="Failed to save logo URL") from e
    
async def delete_client_logo(client_id: int, user_id: str) -> None:
    db = get_supabase()
    client = db.table("clients").select("id, logo_url").eq("id", client_id).eq("user_id", user_id).single().execute()
    
    if not client.data or not client.data.get("logo_url"):
        raise HTTPException(status_code=404, detail="Logo not found")

    logo_url = client.data["logo_url"]
    path = logo_url.replace(f"{R2_PUBLIC_URL}/", "")

    r2 = get_r2_logos_client()
    try:
        r2.delete_object(Bucket=R2_LOGOS_BUCKET_NAME, Key=path)
    except Exception as e:
        logger.error(f"Error deleting logo from R2: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete logo from R2") from e

    db.table("clients").update({"logo_url": None}).eq("id", client_id).eq("user_id", user_id).execute()