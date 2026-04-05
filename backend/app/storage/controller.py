# Copyright © 2026 Jorge Vinagre
# SPDX-License-Identifier: AGPL-3.0-only WITH Commons-Clause
"""Storage-related API endpoints."""

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from .schemas import SaveFileMetadataRequest, GenerateUploadUrlRequest, S3FileResponse, S3UrlResponse   
from .service import generate_upload_url, generate_download_url, list_files, delete_file, save_file_metadata, delete_folder

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/upload/{client_id}/{folder:path}", response_model=S3UrlResponse)
async def create_upload_url(client_id: int, folder: str, request: GenerateUploadUrlRequest, user = Depends(get_current_user)):
    """Generate a pre-signed URL for uploading a file to S3."""

    return await generate_upload_url(client_id, folder, request, user.id)

@router.post("/save-file", status_code=status.HTTP_204_NO_CONTENT)
async def save_file(request: SaveFileMetadataRequest, user = Depends(get_current_user)):
    """Save file metadata to the database after a successful upload."""

    return await save_file_metadata(request, user.id)
    
@router.get("/download/{client_id}/{folder:path}/{file_id}", response_model=S3UrlResponse)
async def create_download_url(client_id: int, folder: str, file_id: int, user = Depends(get_current_user)):
    """Generate a pre-signed URL for downloading a file from S3."""

    return await generate_download_url(client_id, folder, file_id, user.id)

@router.get("/list/{client_id}/{folder:path}", response_model=list[S3FileResponse])
async def get_files(client_id: int, folder: str, user = Depends(get_current_user)):
    """List files in a specific S3 folder for a client."""

    return await list_files(client_id, folder, user.id)

@router.delete("/delete/{client_id}/{folder:path}/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_file(client_id: int, folder: str, file_id: int, user = Depends(get_current_user)):
    """Delete a file from S3 and DB."""

    return await delete_file(client_id, folder, file_id, user.id)

@router.delete("/delete-folder/{client_id}/{folder:path}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_folder(client_id: str, folder: str, user = Depends(get_current_user)):
    """Delete folder and the files inside from S3 and DB."""

    return await delete_folder(client_id, folder, user.id)