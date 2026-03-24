# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""AI-related API endpoints."""

from fastapi import APIRouter, Request

from .schemas import TextRequest, TextResponse, TextVariation
from .service import improve_text

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/improve-text", response_model=TextResponse, tags=["text-improvement"])
async def improve(request: TextRequest, req: Request):
    """Improve the submitted text with AI, returning three variations."""
    improved = await improve_text(request, req)
    return TextResponse(variations=[TextVariation(text=improved)])
    