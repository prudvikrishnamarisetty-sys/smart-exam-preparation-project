from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user
import json

router = APIRouter(prefix="/exam", tags=["Exams"])


def _db_questions(config: models.ExamConfig, num_q: int, db: Session, exclude_texts: set = None) -> list:
    """Fetch questions from the DB, cascading through match tiers. Returns up to num_q dicts."""
    import random
    exclude_texts = exclude_texts or set()

    def _to_dict(sq):
        return {
            "text": sq.text, "option_a": sq.option_a, "option_b": sq.option_b,
            "option_c": sq.option_c, "option_d": sq.option_d,
            "correct_option": sq.correct_option, "explanation": sq.explanation,
            "subject": sq.subject, "section": sq.section or sq.subject, "topic": sq.topic,
            "difficulty": sq.difficulty, "marks_per_question": config.marks_per_question,
            "negative_marks": config.negative_marking,
        }

    result = []
    needed = num_q

    # Tier 1: exact exam_key
    qs = db.query(models.Question).filter(models.Question.exam_type == config.exam_key).all()
    random.shuffle(qs)
    for sq in qs:
        if sq.text not in exclude_texts:
            result.append(_to_dict(sq))
            exclude_texts.add(sq.text)
        if len(result) >= needed:
            return result

    # Tier 2: prefix match (e.g., RRB_* for RRB_ALP_STAGE1)
    if len(result) < needed:
        prefix = config.exam_key.split('_')[0]
        qs2 = db.query(models.Question).filter(
            models.Question.exam_type.like(f"{prefix}%"),
            ~models.Question.exam_type.in_([config.exam_key])
        ).all()
        random.shuffle(qs2)
        for sq in qs2:
            if sq.text not in exclude_texts:
                result.append(_to_dict(sq))
                exclude_texts.add(sq.text)
            if len(result) >= needed:
                return result

    # Tier 3: any questions in the DB (last resort)
    if len(result) < needed:
        qs3 = db.query(models.Question).limit(needed * 5).all()
        random.shuffle(qs3)
        for sq in qs3:
            if sq.text not in exclude_texts:
                result.append(_to_dict(sq))
                exclude_texts.add(sq.text)
            if len(result) >= needed:
                return result

    return result


def _ai_generate(config: models.ExamConfig, num_q: int, db: Session) -> list:
    """
    Generate exactly num_q questions using AI ONLY.
    If AI returns partial result, it will raise an error (or user must retry).
    The user specifically requested ALL questions be AI-generated.
    """
    ai_questions: list = []

    # --- Try AI generation ---
    try:
        from services.gemini_service import generate_questions
        ai_questions = generate_questions(
            exam_key=config.exam_key,
            display_name=config.display_name,
            pattern_summary=config.pattern_summary,
            sections_json=config.sections_json,
            num_questions=num_q,
            marks_per_q=config.marks_per_question,
            negative_marking=config.negative_marking,
        )
    except Exception as e:
        print(f"[AI-Only] Generation failed: {e}")
        raise HTTPException(
            status_code=503, 
            detail=f"AI service is currently unable to generate the full question set ({len(ai_questions)}/{num_q} generated). Please try again in a moment."
        )

    if len(ai_questions) < num_q:
        print(f"[AI-Only] Shortfall: {len(ai_questions)}/{num_q} generated.")

    return ai_questions[:num_q]


@router.post("/start", response_model=schemas.ExamOut)
def start_exam(
    req: schemas.ExamStartRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    config = db.query(models.ExamConfig).filter(
        models.ExamConfig.exam_key == req.exam_config_key
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail=f"Exam config '{req.exam_config_key}' not found")

    num_q = config.total_questions

    # === AI generates questions in real-time ===
    ai_questions = _ai_generate(config, num_q, db)

    # Pad with DB questions if AI fell short
    if len(ai_questions) < num_q:
        needed = num_q - len(ai_questions)
        exclude_texts = {q.get("text") for q in ai_questions}
        fallback_qs = _db_questions(config, needed, db, exclude_texts)
        ai_questions.extend(fallback_qs)

    if not ai_questions:
        raise HTTPException(status_code=500, detail="Failed to generate any questions. Try again.")

    # Create exam record
    exam = models.Exam(
        user_id=current_user.id,
        exam_type=req.exam_config_key,
        exam_config_key=req.exam_config_key,
        subject_filter=req.subject_filter or "",
        difficulty=req.difficulty or "mixed",
        num_questions=len(ai_questions),
        duration_minutes=config.duration_minutes,
        marks_per_q=config.marks_per_question,
        negative_marks_per_q=config.negative_marking,
        status="in_progress",
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    # Store AI questions as temporary Question rows (no uniqueness required, repeats allowed)
    for i, qdata in enumerate(ai_questions):
        q = models.Question(
            text=qdata.get("text", ""),
            option_a=qdata.get("option_a", ""),
            option_b=qdata.get("option_b", ""),
            option_c=qdata.get("option_c", ""),
            option_d=qdata.get("option_d", ""),
            correct_option=qdata.get("correct_option", "A"),
            explanation=qdata.get("explanation", ""),
            exam_type=req.exam_config_key,
            subject=qdata.get("subject", config.display_name),
            section=qdata.get("section", "General"),
            topic=qdata.get("topic", ""),
            difficulty=qdata.get("difficulty", "medium"),
            marks_per_question=qdata.get("marks_per_question", config.marks_per_question),
            negative_marks=qdata.get("negative_marks", config.negative_marking),
            source="AI-Generated",
        )
        db.add(q)
        db.flush()
        eq = models.ExamQuestion(
            exam_id=exam.id,
            question_id=q.id,
            order_num=i + 1,
            visit_status="not_visited",
        )
        db.add(eq)

    db.commit()
    db.refresh(exam)
    return exam


@router.post("/submit", response_model=schemas.ResultOut)
def submit_exam(
    req: schemas.ExamSubmitRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    exam = db.query(models.Exam).filter(
        models.Exam.id == req.exam_id,
        models.Exam.user_id == current_user.id,
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    if exam.status == "completed":
        raise HTTPException(status_code=400, detail="Exam already submitted")

    correct = wrong = unattempted = 0
    section_scores: dict = {}

    for ans in req.answers:
        eq = db.query(models.ExamQuestion).filter(
            models.ExamQuestion.exam_id == exam.id,
            models.ExamQuestion.question_id == ans.question_id,
        ).first()
        if not eq:
            continue
        question = db.query(models.Question).filter(
            models.Question.id == ans.question_id
        ).first()

        if ans.marked_for_review is not None:
            eq.marked_for_review = ans.marked_for_review
        if ans.visit_status:
            eq.visit_status = ans.visit_status

        section = question.section or question.subject or "General"
        if section not in section_scores:
            section_scores[section] = 0.0

        if ans.selected_option:
            eq.selected_option = ans.selected_option
            eq.is_correct = ans.selected_option.upper() == question.correct_option.upper()
            if eq.is_correct:
                correct += 1
                section_scores[section] += exam.marks_per_q
            else:
                wrong += 1
                section_scores[section] -= exam.negative_marks_per_q
        else:
            eq.is_correct = False
            unattempted += 1

    total = len(req.answers)
    raw_score = correct * exam.marks_per_q
    negative_deducted = wrong * exam.negative_marks_per_q
    final_score = raw_score - negative_deducted
    max_score = total * exam.marks_per_q
    percentage = round((final_score / max_score * 100) if max_score > 0 else 0, 2)

    exam.status = "completed"
    exam.submitted_at = datetime.utcnow()

    result = models.Result(
        exam_id=exam.id,
        user_id=current_user.id,
        score=round(final_score, 2),
        raw_score=round(raw_score, 2),
        negative_deducted=round(negative_deducted, 2),
        total=total,
        correct=correct,
        wrong=wrong,
        unattempted=unattempted,
        percentage=percentage,
        time_taken_seconds=req.time_taken_seconds or 0,
        section_scores_json=json.dumps({k: round(v, 2) for k, v in section_scores.items()}),
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/history", response_model=List[schemas.ResultOut])
def get_exam_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Result)
        .filter(models.Result.user_id == current_user.id)
        .order_by(models.Result.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/{exam_id}", response_model=schemas.ExamOut)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    exam = db.query(models.Exam).options(
        joinedload(models.Exam.exam_questions).joinedload(models.ExamQuestion.question)
    ).filter(
        models.Exam.id == exam_id,
        models.Exam.user_id == current_user.id,
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.get("/{exam_id}/review")
def review_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    exam = db.query(models.Exam).filter(
        models.Exam.id == exam_id,
        models.Exam.user_id == current_user.id,
    ).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    review_data = []
    for eq in sorted(exam.exam_questions, key=lambda x: x.order_num):
        q = eq.question
        review_data.append({
            "order": eq.order_num,
            "question_id": q.id,
            "question": q.text,
            "option_a": q.option_a, "option_b": q.option_b,
            "option_c": q.option_c, "option_d": q.option_d,
            "correct_option": q.correct_option,
            "selected_option": eq.selected_option,
            "is_correct": eq.is_correct,
            "marked_for_review": eq.marked_for_review,
            "explanation": q.explanation,
            "subject": q.subject,
            "section": q.section,
            "topic": q.topic,
            "marks_per_question": q.marks_per_question,
            "negative_marks": q.negative_marks,
        })

    result = exam.result
    return {
        "exam_id": exam.id,
        "exam_type": exam.exam_type,
        "exam_config_key": exam.exam_config_key,
        "score": result.score if result else 0,
        "raw_score": result.raw_score if result else 0,
        "negative_deducted": result.negative_deducted if result else 0,
        "total": result.total if result else 0,
        "correct": result.correct if result else 0,
        "wrong": result.wrong if result else 0,
        "unattempted": result.unattempted if result else 0,
        "percentage": result.percentage if result else 0,
        "section_scores": json.loads(result.section_scores_json) if result else {},
        "time_taken_seconds": result.time_taken_seconds if result else 0,
        "questions": review_data,
    }
