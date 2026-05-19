from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import get_current_user

router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/topics")
def get_topics(
    exam_type: str = Query(...),
    subject: str = Query(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Return list of topics for a given exam + subject."""
    topics = (
        db.query(models.Question.topic)
        .filter(models.Question.exam_type == exam_type)
        .filter(models.Question.subject == subject)
        .distinct()
        .all()
    )
    topic_list = [t[0] for t in topics if t[0]]
    # Always return some defaults
    if not topic_list:
        config = db.query(models.ExamConfig).filter(
            models.ExamConfig.exam_key == exam_type
        ).first()
        if config:
            import json
            sections = json.loads(config.sections_json or "[]")
            topic_list = [s["name"] for s in sections] or ["General"]
    return topic_list


@router.post("/fetch")
def fetch_resource(
    payload: dict,
    current_user: models.User = Depends(get_current_user),
):
    """
    AI-powered resource fetching.
    Body: { "exam_type": "GATE_CSE", "subject": "DBMS", "topic": "Normalization" }
    """
    exam_type = payload.get("exam_type", "")
    subject = payload.get("subject", "")
    topic = payload.get("topic", "")

    if not topic:
        raise HTTPException(status_code=400, detail="topic is required")

    try:
        from services.gemini_service import get_resources
        result = get_resources(exam_type, subject, topic)
        return result
    except Exception as e:
        print(f"AI resource fetch failed: {e}. Returning fallback content.")
        fallback_content = f"""# {topic} — Study Notes for {exam_type}

> **Notice:** The AI Service is currently rate-limited. This is static fallback content. 
> Please wait a minute and try again for dynamically generated rich study materials including past 10 years papers.

## 1. Core Concepts
{topic} is an important part of the {subject} syllabus for the {exam_type} examination. 
To master this topic, ensure you review standard textbooks and past papers.

## 2. Key Formulas & Rules
- Review the fundamental principles.
- Memorize key theorems and definitions.

## 3. Practice MCQs
Due to rate limits, specific MCQs are currently unavailable. Try starting a mock exam to practice from the offline database!
"""
        return {"exam_type": exam_type, "subject": subject, "topic": topic, "content": fallback_content}


@router.get("/exam-subjects")
def get_exam_subjects(
    exam_type: str = Query(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all subjects for an exam config."""
    import json
    config = db.query(models.ExamConfig).filter(
        models.ExamConfig.exam_key == exam_type
    ).first()
    if config:
        sections = json.loads(config.sections_json or "[]")
        if sections:
            return [s["name"] for s in sections]
    return ["General"]


@router.post("/past-papers")
def fetch_past_papers(
    payload: dict,
    current_user: models.User = Depends(get_current_user),
):
    """
    AI-powered fetch for past 10 years question papers.
    Body: { "exam_type": "GATE_CSE", "subject": "DBMS", "mode": "exam_only" | "exam_and_subject" }
    """
    exam_type = payload.get("exam_type", "")
    subject = payload.get("subject", "General")
    mode = payload.get("mode", "exam_and_subject")

    try:
        from services.gemini_service import get_past_papers
        result = get_past_papers(exam_type, subject, mode)
        return result
    except Exception as e:
        print(f"AI past papers fetch failed: {e}. Returning fallback content.")
        fallback_content = f"""# Past 5 Years Question Papers — {exam_type}

> **⚠️ Notice:** The AI Service is currently rate-limited. Please wait 1-2 minutes and try again for rich AI-generated past papers with 15+ questions across 5 years.

## Year 2023
**Q1:** Representative question for {exam_type} — {subject}.
- **A)** Option 1
- **B)** Option 2
- **C)** Option 3
- **D)** Option 4
✅ **Answer:** A
📖 **Explanation:** This is a placeholder. Retry when the rate limit resets.

## Year 2022
(Retry in a moment for full 5-year coverage with 15+ questions.)
"""
        return {"exam_type": exam_type, "subject": subject, "topic": "Past 10 Years Papers", "content": fallback_content}
