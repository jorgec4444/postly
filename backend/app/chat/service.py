# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

from .schemas import ChatSessionRequest, ChatSessionResponse, ChatMessageRequest, ChatMessageResponse
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from app.database import get_supabase
from app.config import get_openai_client, MODEL_NAME
import logging

logger = logging.getLogger(__name__)

async def create_new_session(request: ChatSessionRequest, user_id: str) -> ChatSessionResponse:
    db = get_supabase()

    try:
        if request.client_id is not None:
            client = (
                db.table("clients")
                .select("*")
                .eq("user_id", user_id)
                .eq("id", request.client_id)
                .single().execute())
            if not client.data:
                raise HTTPException(status_code=404, detail="Client not found")
        response = db.table("chat_sessions").insert({
                "user_id": user_id,
                "client_id": request.client_id
            }).execute()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating new session: {e}")
    
    return ChatSessionResponse(
        id=response.data[0]["id"],
        client_id=response.data[0]["client_id"],
        created_at=response.data[0]["created_at"]
        )

async def retrieve_session_historic(session_id: str, user_id: str) -> list[ChatMessageResponse]:
    db = get_supabase()

    try:
        session = db.table("chat_sessions").select("id").eq("id", session_id).eq("user_id", user_id).single().execute()
        if not session.data:
            raise HTTPException(status_code=404, detail="Session not found")
        response = (
            db.table("chat_messages")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at").execute()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving historical messages for session {session_id}: {e}")
    
    return [ChatMessageResponse(**msg) for msg in response.data]


async def send_chat_message(session_id: str, request: ChatMessageRequest, user_id: str):
    db = get_supabase()
    open_ai_client = get_openai_client()

    try:
        valid_session = (
            db.table("chat_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", user_id)
            .single().execute()
        )

        if not valid_session.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        brand_voice = None
        if valid_session.data["client_id"]:
            result = (
                db.table("clients")
                .select("brand_voice")
                .eq("id", valid_session.data["client_id"])
                .eq("user_id", user_id)
                .single().execute()
                )
            brand_voice = result.data.get("brand_voice") if result.data else None

        historical = (
            db.table("chat_messages")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .limit(10)
            .execute()
        )

        system = "You are an AI assistant for community managers and social media agencies. Help with content strategy, copywriting, research and any task related to social media management. Always respond in the same language the user writes in."

        if brand_voice:
            system += f"\n\nYou are currently helping with content for a specific client. Here is their brand description, use it to tailor ALL your responses, recommendations and content to match this client's identity and industry:\n\n{brand_voice}"

        messages = [{"role": "system", "content": system}]

        for msg in historical.data:
            messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": request.message})

        async def stream_generator():
            stream = open_ai_client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=800,
                temperature=0.5,
                stream=True,
            )
            
            full_response = ""
            
            db.table("chat_messages").insert({
                "session_id": session_id,
                "role": "user",
                "content": request.message
            }).execute()
            
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    yield delta
            
            db.table("chat_messages").insert({
                "session_id": session_id,
                "role": "assistant",
                "content": full_response
            }).execute()

        return StreamingResponse(stream_generator(), media_type="text/plain")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating new session: {e}")
    

async def get_user_sessions(user_id: str) -> list[ChatSessionResponse]:
    db = get_supabase()
    try:
        response = (
            db.table("chat_sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {e}")
    
    return [ChatSessionResponse(**s) for s in response.data]


async def delete_session(session_id: str, user_id: str) -> None:
    db = get_supabase()
    session = db.table("chat_sessions").select("id").eq("id", session_id).eq("user_id", user_id).single().execute()
    if not session.data:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        db.table("chat_sessions").delete().eq("id", session_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting session: {e}")