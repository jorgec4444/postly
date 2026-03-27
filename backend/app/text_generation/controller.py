# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Text generation-related API endpoints."""

from fastapi import APIRouter, Depends, Request
from app.auth.dependencies import get_optional_user
from .service import save_generation_handler, improve_text
from .schemas import SaveGenerationRequest, TextRequest, TextResponse, TextRequest

router = APIRouter(prefix="/text-generation", tags=["text-generation"])

@router.post("/improve-text", response_model=TextResponse)
async def improve(
    request: TextRequest,
    req: Request,
    user = Depends(get_optional_user)
    ):
    """Improve the submitted text with AI, returning three variations."""

    return await improve_text(request, req, user)

@router.post("/save", response_model=dict)
async def save_generation(request: Request, payload: SaveGenerationRequest):
    """Save a text generation record for analytics (best-effort)."""

    return await save_generation_handler(payload, request)