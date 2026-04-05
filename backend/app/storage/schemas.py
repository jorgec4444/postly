# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Pydantic models for storage-related API endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field

class GenerateUploadUrlRequest(BaseModel):
    """Request body for generating a pre-signed upload URL."""

    file_name: str
    mime_type: str

class SaveFileMetadataRequest(BaseModel):
    """Request body for saving file metadata after upload."""

    file_path: str
    file_name: str
    mime_type: str
    file_size: int
    folder: str
    client_id: int
    user_id: str

class S3FileResponse(BaseModel):
    """Response model for listing files in S3."""

    id: int 
    file_name: str
    file_path: str
    folder: str
    client_id: int
    user_id: str
    mime_type: str
    file_size: int
    created_at: datetime  # ISO 8601 format
