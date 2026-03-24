# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""AI-related data models and validation."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Text to improve")
    style: Optional[str] = Field("professional", description="Improvement style")

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be blank")
        return v.strip()
    
class TextVariation(BaseModel):
    version: str
    text: str
    description: str
    
class TextResponse(BaseModel):
    original: str
    variations: List[TextVariation]