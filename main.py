import os
from dotenv import load_dotenv

# Load .env if present (for GEMINI_API_KEY etc.)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routers import users, questions, exams, dashboard, resources, ai, admin_resources

Base.metadata.create_all(bind=engine)

# --- Migrate: add new columns to existing SQLite DB if they don't exist ---
def _run_migrations():
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "exam.db")
    if not os.environ.get("DATABASE_URL", "sqlite").startswith("sqlite"):
        return
    if not os.path.exists(db_path):
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cursor.fetchall()}
    migrations = {
        "phone":    "ALTER TABLE users ADD COLUMN phone TEXT DEFAULT ''",
        "college":  "ALTER TABLE users ADD COLUMN college TEXT DEFAULT ''",
        "is_admin": "ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0",
        "is_active":"ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1",
    }
    for col, sql in migrations.items():
        if col not in cols:
            print(f"[Migration] Adding column '{col}' to users table")
            cursor.execute(sql)

    cursor.execute("PRAGMA table_info(resources)")
    res_cols = {row[1] for row in cursor.fetchall()}
    res_migrations = {
        "exam_name": "ALTER TABLE resources ADD COLUMN exam_name TEXT DEFAULT ''",
        "file_path": "ALTER TABLE resources ADD COLUMN file_path TEXT DEFAULT ''",
        "file_name": "ALTER TABLE resources ADD COLUMN file_name TEXT DEFAULT ''",
        "tags": "ALTER TABLE resources ADD COLUMN tags TEXT DEFAULT ''",
        "uploaded_by": "ALTER TABLE resources ADD COLUMN uploaded_by INTEGER",
    }
    for col, sql in res_migrations.items():
        if col not in res_cols:
            print(f"[Migration] Adding column '{col}' to resources table")
            cursor.execute(sql)
    conn.commit()
    conn.close()

_run_migrations()

def seed_admin():
    """Create a default admin account on first startup if none exists."""
    from database import SessionLocal
    from auth import get_password_hash
    import models
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            admin = models.User(
                username="admin",
                email="admin@smartexam.local",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                phone="",
                college="SmartExam Platform",
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("[Startup] Default admin created: username=admin, password=admin123")
        elif not admin.is_admin:
            admin.is_admin = True
            db.commit()
            print("[Startup] Existing 'admin' user promoted to admin.")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_admin()
    yield


app = FastAPI(
    title="Smart Examination Platform",
    description="Comprehensive exam preparation for B.Tech CSE/IT & Govt job aspirants",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(exams.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(resources.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(admin_resources.router, prefix="/api")


@app.get("/api")
def root():
    gemini_key_set = bool(os.environ.get("GEMINI_API_KEY", ""))
    return {
        "message": "Smart Examination Platform API v2",
        "docs": "/docs",
        "version": "2.0.0",
        "ai_powered": gemini_key_set,
        "ai_status": "ready" if gemini_key_set else "Set GEMINI_API_KEY in .env to enable AI",
    }

@app.get("/api/health")
def health():
    return {"status": "healthy", "ai_enabled": bool(os.environ.get("GEMINI_API_KEY", ""))}

# Serve frontend static files
if os.path.isdir("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
            
        file_path = os.path.join("dist", full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        return FileResponse(os.path.join("dist", "index.html"))

if __name__ == "__main__":
    import uvicorn
    # Default to 127.0.0.1 on Windows — browsers cannot reach 0.0.0.0 on Windows.
    # Set HOST=0.0.0.0 in your .env only if you need network-wide access.
    default_host = "127.0.0.1" if os.name == "nt" else "0.0.0.0"
    host = os.environ.get("HOST", default_host)
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🚀 Backend running at: http://{host}:{port}")
    print(f"   API docs available: http://{host}:{port}/docs\n")
    uvicorn.run("main:app", host=host, port=port, reload=False)
