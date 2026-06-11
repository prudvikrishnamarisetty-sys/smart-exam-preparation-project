"""
Google Gemini AI Service (using google-genai SDK)
Handles question generation, resource gathering, and chat.
Robust: multi-model fallback + exponential backoff so rate limits never block users.
"""
import os
import json
import re
import time
from google import genai
from google.genai import types
from groq import Groq

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def get_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set.")
    return genai.Client(api_key=GEMINI_API_KEY)

def get_groq_client():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set.")
    return Groq(api_key=GROQ_API_KEY)

def _call_groq(prompt: str, max_retries: int = 5, is_json: bool = False) -> str:
    """
    Call Groq (Llama 3) for lightning-fast text generation.
    Falls back to smaller models if rate limited.
    """
    client = get_groq_client()
    last_err = None
    delays = [1, 2, 4, 8]
    
    if is_json and "json" not in prompt.lower():
        prompt += "\nReturn output in JSON format."

    models_to_try = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]

    for attempt in range(max_retries):
        for model in models_to_try:
            try:
                kwargs = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 8000,
                }
                if is_json:
                    kwargs["response_format"] = {"type": "json_object"}
                    
                chat_completion = client.chat.completions.create(**kwargs)
                text = chat_completion.choices[0].message.content
                if text:
                    return text
            except Exception as e:
                last_err = e
                err_str = str(e).lower()
                if "rate limit" in err_str or "429" in err_str or "503" in err_str:
                    print(f"[Groq:{model}] Rate limit/Busy. Switching model...")
                    continue
                else:
                    print(f"[Groq:{model}] Error: {e}")
                    continue
                    
        wait = delays[min(attempt, len(delays)-1)]
        print(f"[Groq] All models busy. Waiting {wait}s...")
        time.sleep(wait)
                
    raise RuntimeError(f"Groq generation failed after {max_retries} attempts. Last error: {last_err}")

def _call_gemini(prompt: str, max_retries: int = 5, is_json: bool = False) -> str:
    """
    Call Gemini with high persistence for massive parallel processing.
    """
    client = get_client()
    last_err = None
    delays = [2, 4, 8, 16]
    models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]

    for attempt in range(max_retries):
        for model in models:
            try:
                config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=8192)
                if is_json:
                    config.response_mime_type = "application/json"

                response = client.models.generate_content(model=model, contents=prompt, config=config)
                if response.text:
                    return response.text
            except Exception as e:
                last_err = e
                err_str = str(e).lower()
                if any(k in err_str for k in ("429", "quota", "rate", "503")):
                    continue
                continue

        wait = delays[min(attempt, len(delays) - 1)]
        print(f"[Gemini] All models busy. Waiting {wait}s...")
        time.sleep(wait)

    raise RuntimeError(f"Gemini generation failed. Last error: {last_err}")

def _call(prompt: str, max_retries: int = 5, is_json: bool = False) -> str:
    """Default text engine: uses Groq for speed."""
    return _call_groq(prompt, max_retries, is_json)

def _clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    raw = raw.strip().strip("`").strip()
    return raw


def generate_questions(exam_key: str, display_name: str, pattern_summary: str,
                       sections_json: str, num_questions: int,
                       marks_per_q: float, negative_marking: float) -> list[dict]:
    import concurrent.futures

    sections = json.loads(sections_json or "[]")
    section_info = ""
    if sections:
        section_info = "Sections:\n" + "\n".join(
            f"  - {s['name']}: {s['questions']} Qs, +{s['marks_per_q']} marks, -{s['negative']} per wrong"
            for s in sections
        )

    BATCH = 30
    all_valid: list[dict] = []
    seen_texts: set[str] = set()
    num_batches = (num_questions + BATCH - 1) // BATCH

    # Use Groq for 30 or less, Gemini Multithreading for massive exams
    use_groq = (num_questions <= 30)
    engine_name = "Groq" if use_groq else "Gemini Multithreaded"

    def generate_batch(batch_idx):
        target_count = min(BATCH, num_questions - batch_idx * BATCH)
        diversity_hint = f"\nIMPORTANT: This is batch {batch_idx+1}. Ensure maximum diversity of topics, sections, and difficulty levels."
        
        batch_results = []
        max_batch_retries = 5 
        
        for attempt in range(max_batch_retries):
            needed_in_batch = target_count - len(batch_results)
            if needed_in_batch <= 0:
                break
                
            prompt = f"""You are an expert exam question generator for {display_name}.
{section_info}{diversity_hint}

Generate EXACTLY {needed_in_batch} unique MCQ questions strictly following the syllabus of {display_name}.
(Already have {len(batch_results)} questions, need {needed_in_batch} more to reach {target_count})

Return a JSON array of objects with keys: text, option_a, option_b, option_c, option_d, correct_option, subject, section, topic, difficulty, marks_per_question, negative_marks."""
            try:
                raw = _call_groq(prompt, is_json=True, max_retries=2) if use_groq else _call_gemini(prompt, is_json=True, max_retries=3)
                questions = json.loads(raw)
                if not isinstance(questions, list):
                    continue
                    
                for q in questions:
                    if not isinstance(q, dict):
                        continue
                    if "question" in q and "text" not in q: q["text"] = q.pop("question")
                    elif "question_text" in q and "text" not in q: q["text"] = q.pop("question_text")
                    
                    cop = str(q.get("correct_option", "")).strip().upper()
                    if "A" in cop or cop == "OPTION_A": q["correct_option"] = "A"
                    elif "B" in cop or cop == "OPTION_B": q["correct_option"] = "B"
                    elif "C" in cop or cop == "OPTION_C": q["correct_option"] = "C"
                    elif "D" in cop or cop == "OPTION_D": q["correct_option"] = "D"
                    else: q["correct_option"] = "A"

                    required = {"text", "option_a", "option_b", "option_c", "option_d", "correct_option"}
                    text = str(q.get("text", "")).strip()
                    if required.issubset(q.keys()) and len(text) > 15 and text not in seen_texts and not text.lower().startswith("fallback"):
                        seen_texts.add(text)
                        batch_results.append(q)
                
                if len(batch_results) >= target_count:
                    break
                else:
                    print(f"[{engine_name}:Batch{batch_idx+1}] Partial batch: {len(batch_results)}/{target_count}. Retrying...")
            except Exception as e:
                print(f"[{engine_name}:Batch{batch_idx+1}] Attempt {attempt+1} failed: {e}. Retrying...")
                time.sleep(1)
                
        return batch_results

    print(f"[generate_questions] Generating {num_questions} questions via {engine_name}")
    
    workers = 1 if use_groq else 5
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(generate_batch, i) for i in range(num_batches)]
        for future in concurrent.futures.as_completed(futures):
            batch_qs = future.result()
            all_valid.extend(batch_qs)

    return all_valid[:num_questions]


def ask_ai_question(question_text: str, option_a: str, option_b: str,
                    option_c: str, option_d: str, exam_context: str = "") -> dict:
    """
    Inline 'Ask AI' during exam — explains a question.
    Has a detailed offline fallback so the user always gets something useful.
    """
    ctx = f"Exam context: {exam_context}\n" if exam_context else ""
    prompt = f"""{ctx}A student is solving this MCQ during an exam and needs help understanding it:

Question: {question_text}
A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}

Please:
1. Identify the MOST LIKELY correct answer based on your knowledge
2. Explain WHY that answer is correct step-by-step
3. Briefly explain why each other option is wrong
4. Give a quick memory tip or formula if applicable

Keep the response clear, concise, and student-friendly. Format as clean markdown.

Return a JSON object with: likely_answer (A/B/C/D), confidence (high/medium/low), explanation (markdown), and follow_up (list of strings)."""

    try:
        raw = _call(prompt, is_json=True)
        data = json.loads(raw)
        return {
            "likely_answer": data.get("likely_answer", "?"),
            "confidence": data.get("confidence", "medium"),
            "explanation": data.get("explanation", raw),
            "follow_up": data.get("follow_up", []),
        }
    except Exception as e:
        print(f"[ask_ai_question] Error: {e}")
        # Provide a useful offline analysis based on the question content
        return {
            "likely_answer": "?",
            "confidence": "low",
            "explanation": f"""## 🤖 AI Analysis (Offline Mode)

**Question:** {question_text}

**Options:**
- **A)** {option_a}
- **B)** {option_b}
- **C)** {option_c}
- **D)** {option_d}

> ⚠️ The AI service is currently busy with high demand. Here are some tips to solve this on your own:

### 📋 How to Approach This Question:
1. **Read carefully** — identify key terms and what exactly is being asked
2. **Eliminate obviously wrong options** — narrow down to 2 candidates
3. **Apply logic** — use your subject knowledge to pick the best answer
4. **Check for absolutes** — options with "always" or "never" are often wrong

### 💡 Study Tip:
Review your notes on this topic. The AI will be available again shortly — you can retry after a few moments.

_Context: {exam_context}_""",
            "follow_up": [
                "Review the relevant chapter in your notes",
                "Try a similar practice question",
                "Check official study material for this topic",
            ],
        }


def get_resources(exam_type: str, subject: str, topic: str) -> dict:
    prompt = f"""You are an expert educator preparing study material for {exam_type} exam.
Topic: {topic}  |  Subject: {subject}

Create comprehensive study notes:

# {topic} — Complete Study Notes for {exam_type}

## 1. Core Concepts
[Clear explanation]

## 2. Key Formulas & Rules
[All important formulas with derivation hints]

## 3. Solved Examples
[3-5 worked step-by-step examples]

## 4. Common Mistakes to Avoid
[Typical errors]

## 5. Quick Revision Bullets
[10 bullet points for last-minute revision]

## 6. Previous Year Questions (Last 10 Years)
[Format each PYQ as: **Q{{n}}**: question text | **Options**: A) ... B) ... C) ... D) ... | **Answer**: X | **Year**: YYYY | **Explanation**: ...]

## 7. Practice MCQs (5 Questions)
[5 original MCQs with full solutions]

Make all content accurate, exam-specific, and easy to understand."""

    content = _call(prompt)
    return {"exam_type": exam_type, "subject": subject, "topic": topic, "content": content}


def get_past_papers(exam_type: str, subject: str, mode: str = "exam_and_subject") -> dict:
    if mode == "exam_only":
        scope = f"all subjects of the {exam_type} exam"
        header = f"# Past 5 Years Question Papers — {exam_type}"
    else:
        scope = f"{subject} section of the {exam_type} exam"
        header = f"# Past 5 Years Question Papers: {subject} ({exam_type})"

    prompt = f"""You are an expert examiner with deep knowledge of the {exam_type} examination pattern.
Generate a COMPREHENSIVE collection of authentic Previous Year Questions (PYQs) from the {scope}.

{header}

Requirements:
- Cover EXACTLY 5 years: 2020, 2021, 2022, 2023, 2024
- For EACH year, provide EXACTLY 3-4 questions
- Total output must have at least 15 questions
- Make questions AUTHENTIC and matching the real difficulty of {exam_type}
- Include questions from different topics each year
- Every question MUST have all 4 options, the correct answer, and an explanation

Use this EXACT format for each year section:

## 📅 Year [YYYY]

**Q1.** [Full question text here]
- **A)** [Option A]
- **B)** [Option B]
- **C)** [Option C]
- **D)** [Option D]
✅ **Answer:** [A/B/C/D] — [Option text]
📖 **Explanation:** [Clear step-by-step explanation]
🏷️ **Topic:** [Topic name] | **Difficulty:** [Easy/Medium/Hard]

---

(Repeat for Q2, Q3, Q4, Q5)

[Repeat the ## 📅 Year block for ALL 5 years]

Make all questions strictly exam-pattern accurate and educationally valuable."""

    content = _call(prompt)
    return {"exam_type": exam_type, "subject": subject, "topic": "Past 10 Years Papers", "content": content, "mode": mode}


def analyze_media_ai(image_data: bytes, mime_type: str, user_question: str = "") -> dict:
    """Analyze an uploaded image/media file using Gemini Vision."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set.")

    import base64
    client = get_client()

    question_part = f"\n\nUser's question: {user_question}" if user_question.strip() else ""

    prompt = f"""You are an expert AI tutor for competitive exam students.
A student has uploaded an image (could be a question paper, handwritten notes, textbook page, diagram, or MCQ).{question_part}

Please analyze the image and:
1. If it contains exam questions or MCQs — solve each one with full step-by-step explanation
2. If it contains notes or theory — summarize the key concepts clearly
3. If it contains a diagram — explain what it represents
4. If it contains handwritten text — transcribe and explain it
5. If the student asked a specific question about it — answer that directly

Format your response as clean, well-structured markdown with:
- Clear headings for each question/section found
- Step-by-step solutions for any problems
- Key concepts highlighted in **bold**
- Final answers clearly marked

Return ONLY this JSON (no markdown fences):
{{
  "response": "## Your full markdown analysis here...",
  "questions_found": 0,
  "follow_up_questions": ["Follow-up 1?", "Follow-up 2?", "Follow-up 3?"]
}}"""

    image_b64 = base64.b64encode(image_data).decode("utf-8")

    # Try models that support vision
    for model in ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {
                        "parts": [
                            {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                            {"text": prompt}
                        ]
                    }
                ],
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=8192,
                ),
            )
            raw = response.text
            break
        except Exception as e:
            print(f"[analyze_media:{model}] {e}")
            raw = None

    if not raw:
        return {
            "response": "## AI Vision Unavailable\n\nThe AI image analysis service is currently busy. Please try again in a moment.",
            "questions_found": 0,
            "follow_up_questions": ["Try again in a few moments", "Type your question in the chat instead"],
        }

    cleaned = _clean_json(raw)
    try:
        data = json.loads(cleaned)
        return {
            "response": data.get("response", raw),
            "questions_found": data.get("questions_found", 0),
            "follow_up_questions": data.get("follow_up_questions", []),
        }
    except Exception:
        return {
            "response": raw,
            "questions_found": 0,
            "follow_up_questions": [
                "Can you explain this in simpler terms?",
                "What are the key takeaways?",
                "Are there similar exam questions on this topic?",
            ],
        }


def ai_chat_response(message: str, context: str = "") -> dict:
    prompt = f"""You are an expert AI tutor for competitive exams and B.Tech CSE/IT students.
{f'Context: {context}' if context else ''}
User question: {message}

Rules:
1. Always give STEP-BY-STEP explanations, never just final answer
2. For MCQs: explain why correct option is right AND why each wrong option is wrong
3. For coding: Logic → Dry Run → Commented Code → Time/Space Complexity → Edge Cases
4. For concepts: use examples and analogies
5. Use clean markdown formatting

Return a JSON object with: response (full markdown string) and follow_up_questions (list of strings)."""

    try:
        raw = _call(prompt, is_json=True)
        data = json.loads(raw)
        return {
            "response": data.get("response", raw),
            "follow_up_questions": data.get("follow_up_questions", []),
        }
    except Exception as e:
        print(f"[ai_chat_response] Error: {e}")
        return {
            "response": "## 🤖 AI Assistant (Temporarily Busy)\n\nI am currently receiving a high volume of requests and have reached my temporary quota limit. \n\n**To continue:**\n1. Please wait for about 30-60 seconds.\n2. Try asking your question again.\n\nI apologize for the interruption! This usually happens during peak usage times.",
            "follow_up_questions": [
                "Try asking again in a minute",
                "Can you summarize the topic instead?",
                "What are the most important points here?",
            ],
        }


def explain_question_ai(question_text: str, options: dict, correct_option: str,
                        user_answer: str, explanation: str, subject: str, topic: str) -> dict:
    opt_text = {k: v for k, v in options.items()}
    correct_text = opt_text.get(correct_option, "")
    user_text = opt_text.get((user_answer or "").upper(), "Not attempted")
    is_correct = bool(user_answer and user_answer.upper() == correct_option.upper())

    prompt = f"""You are an expert AI tutor. Explain this exam question.

Question: {question_text}
A: {options.get('A', '')}
B: {options.get('B', '')}
C: {options.get('C', '')}
D: {options.get('D', '')}
Correct Answer: {correct_option} — {correct_text}
Student Answer: {user_answer or 'Not attempted'} — {user_text}
Result: {'CORRECT' if is_correct else 'INCORRECT'}
Subject: {subject} | Topic: {topic}
Hint: {explanation}

Return a JSON object with: step1_restatement, step2_concepts, step3_working, step4_answer (all markdown strings) and step5_similar (list of objects with text, option_a, option_b, option_c, option_d, correct_option, explanation)."""

    try:
        raw = _call(prompt, is_json=True)
        return json.loads(raw)
    except Exception:
        return {
            "step1_restatement": f"**Correct Answer:** {correct_option} — {correct_text}",
            "step2_concepts": f"**Subject:** {subject} | **Topic:** {topic}",
            "step3_working": explanation or "See correct option above.",
            "step4_answer": f"**Final Answer: {correct_option}**",
            "step5_similar": [],
        }


def generate_questions_from_text(text: str, num_questions: int, exam_type: str = "General") -> list[dict]:
    """Generate ad-hoc questions from arbitrary text for practice without storing them."""
    prompt = f"""You are an expert examiner for {exam_type}.
Based on the following source material provided by the student, generate exactly {num_questions} Multiple Choice Questions.

Source Material:
\"\"\"{text}\"\"\"

Ensure the questions strictly test the concepts mentioned in the text.
Return a JSON array of objects, where each object has:
- text: The question text
- option_a, option_b, option_c, option_d: The four options
- correct_option: The correct option letter (A, B, C, or D)
- explanation: A brief explanation of why the answer is correct based on the text.
- subject: A short topic string derived from the text.

Only return the JSON array."""
    try:
        raw = _call(prompt, is_json=True, max_retries=2)
        questions = json.loads(raw)
        if isinstance(questions, list):
            # Normalize correct_option to A/B/C/D
            for q in questions:
                cop = str(q.get("correct_option", "")).strip().upper()
                if "A" in cop: q["correct_option"] = "A"
                elif "B" in cop: q["correct_option"] = "B"
                elif "C" in cop: q["correct_option"] = "C"
                elif "D" in cop: q["correct_option"] = "D"
                else: q["correct_option"] = "A"
            return questions
        return []
    except Exception as e:
        print(f"[generate_questions_from_text] Failed: {e}")
        return []
