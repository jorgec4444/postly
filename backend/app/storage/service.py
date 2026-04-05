# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Service layer for storage-related operations."""

from fastapi import HTTPException

from .schemas import S3FileResponse, GenerateUploadUrlRequest, SaveFileMetadataRequest
from app.config import get_r2_client, R2_BUCKET_NAME
from app.database import get_supabase

import logging

logger = logging.getLogger(__name__)

async def generate_upload_url(
        client_id: int, folder: str, upload_request: GenerateUploadUrlRequest, user_id: str
        ) -> str:
    """Generate a pre-signed URL for uploading a file to S3."""

    r2_client = get_r2_client()
    path=f"{user_id}/{client_id}/{folder}/{upload_request.file_name}"

    try:
        upload_generated_url = r2_client.generate_presigned_url(
            "put_object",
            Params={
                'Bucket': R2_BUCKET_NAME,
                'Key': path,
                'ContentType': upload_request.mime_type
                },
            ExpiresIn=900 # URL expires in 15 minutes
            )
    except Exception as e:
        logger.error(f"Error generating pre-signed URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate pre-signed URL") from e
    
    return upload_generated_url

async def save_file_metadata(request: SaveFileMetadataRequest, user_id: str) -> None:
    """Save file metadata to the database after a successful upload."""

    db = get_supabase()
    client = db.table("clients").select("id").eq("id", request.client_id).eq("user_id", user_id).single().execute()
    if not client.data:
        logger.warning(f"Client with ID {request.client_id} not found for user {user_id}")
        raise HTTPException(status_code=404, detail="Client not found when saving file metadata")
    
    try:
        db.table("files").insert({
            "user_id": user_id,
            "client_id": request.client_id,
            "folder": request.folder,
            "file_path": request.file_path,
            "file_name": request.file_name,
            "mime_type": request.mime_type,
            "file_size": request.file_size
        }).execute()
    except Exception as e:
        logger.error(f"Error saving file metadata: {e}")
        raise HTTPException(status_code=500, detail="Failed to save file metadata") from e
    
    return None

async def generate_download_url(client_id: int, folder: str, file_id: int, user_id: str) -> str:
    """Generate a pre-signed URL for downloading a file from S3."""

    r2_client = get_r2_client()
    db = get_supabase()
    file = db.table("files").select("file_path").eq("id", file_id).eq("client_id", client_id).eq("user_id", user_id).single().execute()

    if not file.data:
        logger.warning(f"File with ID {file_id} not found for client {client_id} and user {user_id}")
        raise HTTPException(status_code=404, detail="File not found when generating download URL")
    
    path = file.data["file_path"]

    try:
        download_generated_url = r2_client.generate_presigned_url(
            "get_object",
            Params={'Bucket': R2_BUCKET_NAME, 'Key': path},
            ExpiresIn=900 # URL expires in 15 minutes
            )
    except Exception as e:
        logger.error(f"Error generating pre-signed URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate pre-signed URL during download") from e

    return download_generated_url

async def list_files(client_id: int, folder: str, user_id: str) -> list[S3FileResponse]:
    """List files in a specific S3 folder for a client."""
    
    db = get_supabase()
    try:
        files_list = db.table("files").select("*").eq("client_id", client_id).eq("folder", folder).eq("user_id", user_id).execute()
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail="Failed to list files") from e
    
    return [S3FileResponse(**file_data) for file_data in files_list.data]

async def delete_file(client_id: int, folder: str, file_id: int, user_id: str) -> None:
    """Delete a file from S3."""
    
    r2_client = get_r2_client()
    db = get_supabase()

    file = db.table("files").select("file_path").eq("client_id", client_id).eq("folder", folder).eq("user_id", user_id).eq("id", file_id).single().execute()

    if not file.data:
        logger.warning(f"File with ID {file_id} not found for client {client_id} and user {user_id}")
        raise HTTPException(status_code=404, detail="File not found when deleting")

    try:
        r2_client.delete_object(Bucket=R2_BUCKET_NAME, Key=file.data["file_path"])
    except Exception as e:
        logger.error(f"Error deleting file from S3: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete file from S3") from e

    try:
        db.table("files").delete().eq("id", file_id).eq("client_id", client_id).eq("user_id", user_id).execute()
    except Exception as e:
        logger.error(f"Error deleting file metadata: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete file metadata") from e

    return None