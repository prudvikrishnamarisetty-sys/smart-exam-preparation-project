"""
Admin router: Resource file uploads (PDF, images, etc.) + resource management.
"""
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import get_current_admin, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf": "PDF",
    "image/jpeg": "Image",
    "image/png": "Image",
    "image/gif": "Image",
    "image/webp": "Image",
    "video/mp4": "Video",
    "application/msword": "Document",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Document",
}


@router.get("/resources/exam-types")
def get_resource_exam_types(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Admin: get all exam configs for the resource upload dropdown."""
    configs = db.query(models.ExamConfig).order_by(models.ExamConfig.category, models.ExamConfig.display_name).all()
    return [
        {
            "exam_key": c.exam_key,
            "display_name": c.display_name,
            "category": c.category,
            "icon": c.icon,
        }
        for c in configs
    ]


@router.post("/resources/upload")
async def admin_upload_resource(
    file: UploadFile = File(...),
    title: str = Form(...),
    exam_type: str = Form(""),
    exam_name: str = Form(""),
    subject: str = Form(""),
    description: str = Form(""),
    tags: str = Form(""),
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Admin: upload a PDF, image, or document as a study resource."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"File type '{file.content_type}' not allowed. Use PDF, image, or document.")

    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:  # 50 MB limit
        raise HTTPException(status_code=400, detail="File too large (max 50 MB).")

    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOADS_DIR, unique_name)
    with open(save_path, "wb") as f:
        f.write(contents)

    resource = models.Resource(
        title=title,
        exam_type=exam_type,
        exam_name=exam_name or exam_type.replace("_", " "),
        subject=subject,
        description=description,
        file_path=unique_name,
        file_name=file.filename or unique_name,
        file_type=ALLOWED_TYPES.get(file.content_type, "Document"),
        tags=tags,
        uploaded_by=admin.id,
        is_free=True,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return {
        "id": resource.id,
        "title": resource.title,
        "file_name": resource.file_name,
        "file_type": resource.file_type,
        "message": "Resource uploaded successfully"
    }


@router.delete("/resources/{resource_id}")
def admin_delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Admin: delete an uploaded resource."""
    res = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    if res.file_path:
        full_path = os.path.join(UPLOADS_DIR, res.file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
    db.delete(res)
    db.commit()
    return {"message": f"Resource '{res.title}' deleted"}


@router.get("/resources")
def admin_list_resources(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    """Admin: list all uploaded resources."""
    resources = db.query(models.Resource).order_by(models.Resource.created_at.desc()).all()
    return [_resource_to_dict(r) for r in resources]


# ── Public / User endpoints (search & download) ──────────────────────────────

@router.get("/public/resources")
def list_resources(
    exam_type: Optional[str] = None,
    subject: Optional[str] = None,
    file_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Users: search and browse uploaded resources."""
    q = db.query(models.Resource)
    if exam_type:
        q = q.filter(models.Resource.exam_type == exam_type)
    if subject:
        q = q.filter(models.Resource.subject.ilike(f"%{subject}%"))
    if file_type:
        q = q.filter(models.Resource.file_type == file_type)
    if search:
        term = f"%{search}%"
        q = q.filter(
            models.Resource.title.ilike(term) |
            models.Resource.description.ilike(term) |
            models.Resource.tags.ilike(term) |
            models.Resource.exam_name.ilike(term) |
            models.Resource.exam_type.ilike(term)
        )
    resources = q.order_by(models.Resource.created_at.desc()).limit(100).all()
    return [_resource_to_dict(r) for r in resources]


@router.get("/public/resources/{resource_id}/download")
def download_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    token: Optional[str] = None,
):
    """
    Download/view a resource file.
    Authenticates via ?token=<jwt> query parameter (for browser tab opens from <a href>).
    The frontend appends the JWT token to the URL automatically.
    """
    from auth import verify_token

    # Validate via query-param token (frontend always appends it)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please log in first.",
        )
    try:
        verify_token(token, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session. Please log in again.")

    res = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Resource not found")
    if not res.file_path:
        raise HTTPException(status_code=404, detail="No file attached to this resource")
    full_path = os.path.join(UPLOADS_DIR, res.file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    ext = os.path.splitext(res.file_path)[1].lower()
    ext_map = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp",
        ".mp4": "video/mp4",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    media_type = ext_map.get(ext, "application/octet-stream")

    return FileResponse(
        path=full_path,
        filename=res.file_name or res.file_path,
        media_type=media_type,
    )



def _resource_to_dict(r: models.Resource) -> dict:
    return {
        "id": r.id,
        "title": r.title,
        "exam_type": r.exam_type,
        "exam_name": r.exam_name,
        "subject": r.subject,
        "description": r.description,
        "file_name": r.file_name,
        "file_type": r.file_type,
        "tags": r.tags,
        "has_file": bool(r.file_path),
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }
