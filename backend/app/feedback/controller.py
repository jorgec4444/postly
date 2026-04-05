# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Feedback-related API endpoints."""

import logging

from fastapi import APIRouter, Depends, Request
from app.utils.http import get_user_ip
from app.auth.dependencies import get_optional_user
from .schemas import FeedbackRequest
from .service import feedback_logger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/save", response_model=dict)
async def send_feedback(body: FeedbackRequest, req: Request, user = Depends(get_optional_user)):
    """Store user feedback."""

    user_id = user.id if user else None
    user_ip = get_user_ip(req)
    logger.info(f"Received feedback from {'user ' + user_id if user_id else 'IP ' + user_ip}")

    feedback_logger.log_feedback(
        ip=user_ip,
        feedback=body.feedback,
        user_id=user_id
    )
    return {"success": True, "message": "Feedback received — thank you!"}