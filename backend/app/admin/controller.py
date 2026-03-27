# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Admin-related API endpoints (protected by ADMIN_API_KEY)."""

import logging

from fastapi import APIRouter, HTTPException
from app.config import ADMIN_API_KEY
from .service import get_stats

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"], include_in_schema=False)

@router.get("/stats")
async def admin_stats(api_key: str | None = None):
    """Aggregated usage statistics (protected by ADMIN_API_KEY)."""
    if not ADMIN_API_KEY or api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return get_stats()