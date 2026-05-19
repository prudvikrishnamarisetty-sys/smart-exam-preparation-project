from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post("/explain", response_model=schemas.AIExplainResponse)
def explain_question(
    req: schemas.AIExplainRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    q = db.query(models.Question).filter(models.Question.id == req.question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    options = {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d}

    try:
        from services.gemini_service import explain_question_ai
        result = explain_question_ai(
            question_text=q.text,
            options=options,
            correct_option=q.correct_option,
            user_answer=req.user_answer,
            explanation=q.explanation,
            subject=q.subject,
            topic=q.topic,
        )
    except Exception as e:
        print(f"AI Explain failed: {e}. Returning fallback content.")
        result = {
            "step1_restatement": f"**Correct Answer:** {q.correct_option}",
            "step2_concepts": f"**Notice:** Detailed AI explanation is currently unavailable due to high server load or rate limits. Please try again in a minute.",
            "step3_working": q.explanation or "No static explanation provided in the database.",
            "step4_answer": f"**Final Answer: {q.correct_option}**",
            "step5_similar": [],
        }

    return schemas.AIExplainResponse(
        step1_restatement=result.get("step1_restatement", ""),
        step2_concepts=result.get("step2_concepts", ""),
        step3_working=result.get("step3_working", ""),
        step4_answer=result.get("step4_answer", ""),
        step5_similar=result.get("step5_similar", []),
    )


@router.post("/ask")
def ask_ai_inline(
    req: dict,
    current_user: models.User = Depends(get_current_user),
):
    """
    Inline 'Ask AI' during an exam. Works with AI-generated questions (no DB required).
    Body: { question_text, option_a, option_b, option_c, option_d, exam_context? }
    """
    question_text = req.get("question_text", "").strip()
    if not question_text:
        raise HTTPException(status_code=400, detail="question_text is required")

    try:
        from services.gemini_service import ask_ai_question
        result = ask_ai_question(
            question_text=question_text,
            option_a=req.get("option_a", ""),
            option_b=req.get("option_b", ""),
            option_c=req.get("option_c", ""),
            option_d=req.get("option_d", ""),
            exam_context=req.get("exam_context", ""),
        )
        return result
    except Exception as e:
        print(f"[/ai/ask] Failed: {e}")
        return {
            "likely_answer": "?",
            "confidence": "low",
            "explanation": (
                "## AI Analysis\n\n"
                "The AI assistant is currently busy or rate-limited. "
                "Please try again in a moment.\n\n"
                f"**Question:** {question_text}"
            ),
            "follow_up": [],
        }


@router.post("/chat", response_model=schemas.AIChatResponse)
def ai_chat(
    req: schemas.AIChatRequest,
    current_user: models.User = Depends(get_current_user),
):
    try:
        from services.gemini_service import ai_chat_response
        result = ai_chat_response(
            message=req.message,
            context=req.context or "",
        )
    except Exception as e:
        print(f"AI Chat failed: {e}. Returning fallback content.")
        result = {
            "response": "⚠️ **AI Assistant is currently rate-limited.**\n\nI am experiencing a high volume of requests and have hit my quota limit. Please wait for a minute and try asking again.",
            "follow_up_questions": ["Try again later", "Check connection"],
        }

    return schemas.AIChatResponse(
        response=result.get("response", ""),
        follow_up_questions=result.get("follow_up_questions", []),
    )


ALLOWED_MIMES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/heic", "image/heif"}

@router.post("/analyze-media")
async def analyze_media(
    file: UploadFile = File(...),
    question: Optional[str] = Form(""),
    current_user: models.User = Depends(get_current_user),
):
    """
    Upload an image (question paper, notes, diagram) and get an AI explanation.
    Optionally send a question about the image via the `question` form field.
    """
    if file.content_type not in ALLOWED_MIMES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Please upload a JPEG, PNG, GIF, or WebP image."
        )

    # Limit file size to 10 MB
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10 MB.")

    try:
        from services.gemini_service import analyze_media_ai
        result = analyze_media_ai(
            image_data=contents,
            mime_type=file.content_type,
            user_question=question or "",
        )
        return result
    except Exception as e:
        print(f"AI media analysis failed: {e}")
        return {
            "response": f"⚠️ **Could not analyze the image.** The AI is currently rate-limited or unavailable. Please try again in a moment.",
            "questions_found": 0,
            "follow_up_questions": ["Try again in a moment", "Ask a text question instead"],
        }
