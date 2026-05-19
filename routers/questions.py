from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/exam-configs", response_model=List[schemas.ExamConfigOut])
def get_exam_configs(db: Session = Depends(get_db)):
    return db.query(models.ExamConfig).all()


@router.get("/exam-types")
def get_exam_types(db: Session = Depends(get_db)):
    types = db.query(models.Question.exam_type).distinct().all()
    return [t[0] for t in types if t[0]]


@router.get("/subjects")
def get_subjects(exam_type: str = Query(...), db: Session = Depends(get_db)):
    subjects = (
        db.query(models.Question.subject)
        .filter(models.Question.exam_type == exam_type)
        .distinct()
        .all()
    )
    return [s[0] for s in subjects if s[0]]


@router.get("/sections")
def get_sections(exam_type: str = Query(...), db: Session = Depends(get_db)):
    sections = (
        db.query(models.Question.section)
        .filter(models.Question.exam_type == exam_type)
        .distinct()
        .all()
    )
    return [s[0] for s in sections if s[0]]


@router.get("/unseen-count")
def get_unseen_count(
    exam_key: str = Query(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    seen_ids = (
        db.query(models.UserSeenQuestion.question_id)
        .filter(
            models.UserSeenQuestion.user_id == current_user.id,
            models.UserSeenQuestion.exam_key == exam_key,
        )
        .subquery()
    )
    total = db.query(models.Question).filter(models.Question.exam_type == exam_key).count()
    unseen = (
        db.query(models.Question)
        .filter(
            models.Question.exam_type == exam_key,
            ~models.Question.id.in_(seen_ids),
        )
        .count()
    )
    return {"exam_key": exam_key, "total": total, "unseen": unseen, "seen": total - unseen}


@router.get("/", response_model=List[schemas.QuestionOut])
def get_questions(
    exam_type: Optional[str] = None,
    subject: Optional[str] = None,
    section: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    q = db.query(models.Question)
    if exam_type:
        q = q.filter(models.Question.exam_type == exam_type)
    if subject:
        q = q.filter(models.Question.subject == subject)
    if section:
        q = q.filter(models.Question.section == section)
    return q.limit(limit).all()
