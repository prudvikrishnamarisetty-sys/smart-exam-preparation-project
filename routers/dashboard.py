from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    results = (
        db.query(models.Result)
        .filter(models.Result.user_id == current_user.id)
        .order_by(models.Result.created_at.desc())
        .all()
    )

    if not results:
        return {
            "total_exams": 0,
            "avg_percentage": 0,
            "best_score": 0,
            "worst_score": 0,
            "total_questions_attempted": 0,
            "strong_subjects": [],
            "weak_subjects": [],
            "recent_results": [],
            "exam_wise_stats": [],
            "performance_trend": [],
        }

    total_exams = len(results)
    avg_pct = sum((r.percentage or 0) for r in results) / total_exams
    best = max((r.percentage or 0) for r in results)
    worst = min((r.percentage or 0) for r in results)
    total_q = sum((r.total or 0) for r in results)

    # Subject-wise analysis
    subject_stats = {}
    for r in results:
        exam = db.query(models.Exam).filter(models.Exam.id == r.exam_id).first()
        if not exam:
            continue
        for eq in exam.exam_questions:
            q = eq.question
            if not q:
                continue
            subj = q.subject or "Unknown"
            if subj not in subject_stats:
                subject_stats[subj] = {"correct": 0, "total": 0}
            subject_stats[subj]["total"] += 1
            if eq.is_correct:
                subject_stats[subj]["correct"] += 1

    strong = []
    weak = []
    for subj, stats in subject_stats.items():
        pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        if pct >= 65:
            strong.append(subj)
        elif pct < 40:
            weak.append(subj)

    # Exam-wise stats
    exam_types_stats = {}
    for r in results:
        exam = db.query(models.Exam).filter(models.Exam.id == r.exam_id).first()
        if not exam:
            continue
        et = exam.exam_type
        if et not in exam_types_stats:
            exam_types_stats[et] = {"count": 0, "total_pct": 0, "best": 0}
        exam_types_stats[et]["count"] += 1
        exam_types_stats[et]["total_pct"] += (r.percentage or 0)
        exam_types_stats[et]["best"] = max(exam_types_stats[et]["best"], (r.percentage or 0))

    exam_wise = [
        {
            "exam_type": et,
            "exams_taken": s["count"],
            "avg_percentage": round(s["total_pct"] / s["count"], 2),
            "best_percentage": s["best"],
        }
        for et, s in exam_types_stats.items()
    ]

    # Performance trend (last 10)
    trend = [
        {
            "exam_id": r.exam_id,
            "percentage": r.percentage or 0,
            "score": r.score or 0,
            "total": r.total or 0,
            "date": r.created_at.isoformat() if r.created_at else "",
        }
        for r in results[:10]
    ]

    recent = []
    for r in results[:5]:
        if r.section_scores_json is None:
            r.section_scores_json = "{}"
        recent.append(schemas.ResultOut.model_validate(r))

    return {
        "total_exams": total_exams,
        "avg_percentage": round(avg_pct, 2),
        "best_score": best,
        "worst_score": worst,
        "total_questions_attempted": total_q,
        "strong_subjects": strong[:5],
        "weak_subjects": weak[:5],
        "recent_results": recent,
        "exam_wise_stats": exam_wise,
        "performance_trend": trend,
    }


@router.get("/subject-analysis")
def subject_analysis(
    exam_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = (
        db.query(models.ExamQuestion)
        .join(models.Exam)
        .filter(models.Exam.user_id == current_user.id)
        .filter(models.Exam.status == "completed")
    )
    if exam_type:
        query = query.filter(models.Exam.exam_type == exam_type)

    exam_questions = query.all()

    subject_data = {}
    for eq in exam_questions:
        q = eq.question
        if not q:
            continue
        subj = q.subject or "Unknown"
        if subj not in subject_data:
            subject_data[subj] = {"correct": 0, "wrong": 0, "unattempted": 0, "total": 0}
        subject_data[subj]["total"] += 1
        if eq.selected_option is None:
            subject_data[subj]["unattempted"] += 1
        elif eq.is_correct:
            subject_data[subj]["correct"] += 1
        else:
            subject_data[subj]["wrong"] += 1

    return [
        {
            "subject": subj,
            "correct": d["correct"],
            "wrong": d["wrong"],
            "unattempted": d["unattempted"],
            "total": d["total"],
            "percentage": round(d["correct"] / d["total"] * 100, 2) if d["total"] > 0 else 0,
        }
        for subj, d in subject_data.items()
    ]
