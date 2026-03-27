# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Feedback-related API endpoints."""

import logging

from fastapi import APIRouter, Request
from datetime import datetime
from app.utils.http import get_client_ip
from .schemas import FeedbackRequest
from .service import feedback_logger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/save", response_model=dict)
async def send_feedback(body: FeedbackRequest, req: Request):
    """Store user feedback."""
    logger.info(f"Received feedback from IP {get_client_ip(req)}")
    feedback_logger.log_feedback(
        ip=get_client_ip(req),
        feedback=body.feedback,
        timestamp=datetime.now().isoformat(),
    )
    return {"success": True, "message": "Feedback received — thank you!"}