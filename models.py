from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, default="")
    phone = Column(String, default="")
    college = Column(String, default="")
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    exams = relationship("Exam", back_populates="user")
    results = relationship("Result", back_populates="user")
    seen_questions = relationship("UserSeenQuestion", back_populates="user")


class ExamConfig(Base):
    """Official exam pattern configuration."""
    __tablename__ = "exam_configs"
    id = Column(Integer, primary_key=True, index=True)
    exam_key = Column(String, unique=True, index=True)
    display_name = Column(String, nullable=False)
    # GOVT_IT, BTECH_LANG, CORE_CS, CLOUD_DEVOPS, COMPANY
    category = Column(String, default="GOVT_IT")
    total_questions = Column(Integer, default=100)
    total_marks = Column(Float, default=100.0)
    duration_minutes = Column(Integer, default=60)
    negative_marking = Column(Float, default=0.0)   # deducted per wrong answer
    marks_per_question = Column(Float, default=1.0)
    sections_json = Column(Text, default="[]")       # JSON list of section dicts
    pattern_summary = Column(String, default="")     # e.g. "100 Qs | 200 Marks | 60 min | -0.50"
    icon = Column(String, default="📄")
    description = Column(Text, default="")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)   # "A", "B", "C", "D"
    explanation = Column(Text, default="")
    exam_type = Column(String, index=True)            # matches ExamConfig.exam_key
    subject = Column(String, index=True)
    section = Column(String, index=True, default="")  # section within exam
    topic = Column(String, index=True, default="")
    sub_topic = Column(String, default="")
    difficulty = Column(String, default="medium")
    year = Column(Integer, nullable=True)
    shift = Column(String, default="")
    marks_per_question = Column(Float, default=1.0)
    negative_marks = Column(Float, default=0.0)
    source = Column(String, default="")
    exam_questions = relationship("ExamQuestion", back_populates="question")
    seen_by = relationship("UserSeenQuestion", back_populates="question")


class UserSeenQuestion(Base):
    """Tracks which questions each user has seen per exam — enforces no-repeat policy."""
    __tablename__ = "user_seen_questions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_key = Column(String, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    seen_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="seen_questions")
    question = relationship("Question", back_populates="seen_by")


class Exam(Base):
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    exam_type = Column(String)
    exam_config_key = Column(String, default="")
    subject_filter = Column(String, default="")
    difficulty = Column(String, default="mixed")
    num_questions = Column(Integer, default=30)
    duration_minutes = Column(Integer, default=60)
    marks_per_q = Column(Float, default=1.0)
    negative_marks_per_q = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="in_progress")
    user = relationship("User", back_populates="exams")
    exam_questions = relationship("ExamQuestion", back_populates="exam")
    result = relationship("Result", back_populates="exam", uselist=False)


class ExamQuestion(Base):
    __tablename__ = "exam_questions"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_option = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    order_num = Column(Integer, default=0)
    marked_for_review = Column(Boolean, default=False)
    # not_visited | visited | answered | marked_review | answered_marked
    visit_status = Column(String, default="not_visited")
    exam = relationship("Exam", back_populates="exam_questions")
    question = relationship("Question", back_populates="exam_questions")


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float, default=0)             # final after negative marks
    raw_score = Column(Float, default=0)         # correct * marks_per_q
    negative_deducted = Column(Float, default=0)
    total = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)
    unattempted = Column(Integer, default=0)
    percentage = Column(Float, default=0)
    time_taken_seconds = Column(Integer, default=0)
    section_scores_json = Column(Text, default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    exam = relationship("Exam", back_populates="result")
    user = relationship("User", back_populates="results")


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    exam_type = Column(String, index=True, default="")
    exam_name = Column(String, default="")   # human-readable exam name
    subject = Column(String, default="")
    description = Column(Text, default="")
    content = Column(Text, default="")
    url = Column(String, default="")
    file_path = Column(String, default="")   # server-side stored file path
    file_name = Column(String, default="")   # original file name
    file_type = Column(String, default="Notes")  # PDF, Image, Notes, Video
    tags = Column(String, default="")        # comma-separated search tags
    is_free = Column(Boolean, default=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

