# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=500, description="Text to improve")
    style: Optional[str] = Field("professional", description="Improvement style")
    client_id: int | None = Field(None, description="Optional client ID for brand voice context")
    temperature: float = Field(0.8, ge=0.0, le=1.0, description="Creativity level (0.0-1.0)")

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be blank")
        return v.strip()
    
    
class TextVariation(BaseModel):
    version: str = Field(..., description="Version label for the variation (e.g., 'Variation 1')")
    text: str = Field(..., description="The improved text variation")
    description: str = Field(..., description="Description of the improvement style applied to this variation")
    

class TextResponse(BaseModel):
    original: str = Field(..., description="The original input text")
    variations: List[TextVariation] = Field(..., description="List of improved text variations with descriptions")


class SaveGenerationRequest(BaseModel):
    original_text: str = Field(..., description="The original text that was improved")
    selected_text: str = Field(..., description="The improved text that the user selected")
    style: str = Field(..., description="The style of improvement applied to the selected text")
    client_id: Optional[int] = Field(None, description="Optional client ID associated with the generation")
    platform: str | None = Field(None, description="Optional platform information for the generation history")


class GenerationsResponse(BaseModel):
    id: int = Field(..., description="Generation ID")
    ip: str | None = Field(None, description="IP address of the request")
    text_original: str = Field(..., description="The original text that was improved")
    text_improved: str = Field(..., description="The improved text")
    style: str = Field(..., description="The style of improvement applied")
    created_at: datetime = Field(..., description="Timestamp of when the generation was created")
    client_id: Optional[int] | None = Field(None, description="Optional client ID associated with the generation")
    platform: Optional[str] | None = Field(None, description="Optional platform information for the generation history")

    model_config = {"from_attributes": True}