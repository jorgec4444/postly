# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

from fastapi import APIRouter, Depends, status
from app.auth.dependencies import get_current_user
from .schemas import ChatMessageRequest, ChatMessageResponse, ChatSessionRequest, ChatSessionResponse
from . import service 
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(get_current_user)])

@router.post("/session", response_model=ChatSessionResponse)
async def create_session(request: ChatSessionRequest, user = Depends(get_current_user)):
    return await service.create_new_session(request, user.id)

@router.get("/session/{session_id}/messages", response_model=list[ChatMessageResponse])
async def get_session_historic(session_id: str, user = Depends(get_current_user)):
    return await service.retrieve_session_historic(session_id, user.id)

@router.post("/session/{session_id}/messages")
async def send_message(session_id: str, request: ChatMessageRequest, user = Depends(get_current_user)):
    return await service.send_chat_message(session_id, request, user.id)

@router.get("/sessions", response_model=list[ChatSessionResponse])
async def get_sessions(user = Depends(get_current_user)):
    return await service.get_user_sessions(user.id)

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: str, user = Depends(get_current_user)):
    return await service.delete_session(session_id, user.id)