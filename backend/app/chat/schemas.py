# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Pydantic schemas for chat-related API endpoints."""

from pydantic import BaseModel
from datetime import datetime

class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

class ChatSessionRequest(BaseModel):
    client_id: int | None = None

class ChatSessionResponse(BaseModel):
    id: str
    client_id: int | None
    created_at: datetime