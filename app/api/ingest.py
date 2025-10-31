"""API endpoints for data ingestion."""

from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    """Accept and acknowledge uploaded files for ingestion."""
    contents = await file.read()
    size_kb = len(contents) / 1024 if contents else 0
    return {
        "filename": file.filename,
        "content_type": file.content_type or "unknown",
        "size_kb": f"{size_kb:.2f}",
        "status": "received",
    }
