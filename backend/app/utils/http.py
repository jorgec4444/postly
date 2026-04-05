# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

"""HTTP-related utilities for FastAPI endpoints."""
from fastapi import Request

def get_user_ip(request: Request) -> str:
    """Extract the real client IP, respecting X-Forwarded-For (Railway/proxies)."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host