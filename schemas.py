from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ---------- Auth ----------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = ""
    phone: Optional[str] = ""
    college: Optional[str] = ""


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    college: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: str
    college: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUserOut(UserOut):
    is_active: bool
    # total exams not queryable from schema; computed separately
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Exam Config ----------
class ExamConfigOut(BaseModel):
    id: int
    exam_key: str
    display_name: str
    category: str
    total_questions: int
    total_marks: float
    duration_minutes: int
    negative_marking: float
    marks_per_question: float
    sections_json: str
    pattern_summary: str
    icon: str
    description: str

    class Config:
        from_attributes = True


# ---------- Questions ----------
class QuestionOut(BaseModel):
    id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    exam_type: str
    subject: str
    section: str
    topic: str
    difficulty: str
    year: Optional[int]
    marks_per_question: float
    negative_marks: float

    class Config:
        from_attributes = True


class QuestionWithAnswer(QuestionOut):
    correct_option: str
    explanation: str


# ---------- Exams ----------
class ExamStartRequest(BaseModel):
    exam_config_key: str
    subject_filter: Optional[str] = ""
    difficulty: Optional[str] = "mixed"


class ExamQuestionOut(BaseModel):
    id: int
    question_id: int
    question: QuestionOut
    order_num: int
    selected_option: Optional[str]
    marked_for_review: bool
    visit_status: str

    class Config:
        from_attributes = True


class ExamOut(BaseModel):
    id: int
    exam_type: str
    exam_config_key: str
    difficulty: str
    num_questions: int
    duration_minutes: int
    marks_per_q: float
    negative_marks_per_q: float
    started_at: datetime
    status: str
    exam_questions: List[ExamQuestionOut]

    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: Optional[str] = None
    marked_for_review: Optional[bool] = False
    visit_status: Optional[str] = "visited"


class ExamSubmitRequest(BaseModel):
    exam_id: int
    answers: List[AnswerSubmit]
    time_taken_seconds: Optional[int] = 0


# ---------- Results ----------
class ResultOut(BaseModel):
    id: int
    exam_id: int
    score: float
    raw_score: float
    negative_deducted: float
    total: int
    correct: int
    wrong: int
    unattempted: int
    percentage: float
    time_taken_seconds: int
    section_scores_json: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Dashboard ----------
class DashboardStats(BaseModel):
    total_exams: int
    avg_percentage: float
    best_score: float
    worst_score: float
    total_questions_attempted: int
    strong_subjects: List[str]
    weak_subjects: List[str]
    recent_results: List[ResultOut]
    exam_wise_stats: List[dict]
    performance_trend: List[dict]


# ---------- Resources ----------
class ResourceOut(BaseModel):
    id: int
    title: str
    exam_type: str
    subject: str
    description: str
    content: str
    url: str
    file_type: str
    is_free: bool

    class Config:
        from_attributes = True


class ResourceRequestCreate(BaseModel):
    exam_type: str
    subject: Optional[str] = ""
    topic: Optional[str] = ""
    message: Optional[str] = ""


class ResourceRequestOut(BaseModel):
    id: int
    user_id: int
    exam_type: str
    subject: str
    topic: str
    message: str
    status: str
    created_at: datetime
    user_name: Optional[str] = ""

    class Config:
        from_attributes = True


# ---------- AI ----------
class AIExplainRequest(BaseModel):
    question_id: int
    user_answer: Optional[str] = None


class AIChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""


class AIExplainResponse(BaseModel):
    step1_restatement: str
    step2_concepts: str
    step3_working: str
    step4_answer: str
    step5_similar: List[dict]


class AIChatResponse(BaseModel):
    response: str
    follow_up_questions: List[str]


class AIGenerateFromTextRequest(BaseModel):
    text: str
    num_questions: Optional[int] = 5
    exam_type: Optional[str] = "General"
