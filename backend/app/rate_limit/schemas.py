# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

from pydantic import BaseModel

class RateLimitStatus(BaseModel):
    allowed: bool
    used: int
    remaining: int
    limit: int
    reset_at: str