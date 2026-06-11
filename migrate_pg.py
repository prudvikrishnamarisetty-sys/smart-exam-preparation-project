import os
import sys
from dotenv import load_dotenv

load_dotenv(".env")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL or "sqlite" in DATABASE_URL:
    print("Not a postgres database")
    sys.exit(0)

# Replace postgres:// with postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

from sqlalchemy import create_engine, text

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS college VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE;"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;"))
        
        # also for resources
        conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS exam_name VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS file_path VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS file_name VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS tags VARCHAR DEFAULT '';"))
        conn.execute(text("ALTER TABLE resources ADD COLUMN IF NOT EXISTS uploaded_by INTEGER;"))
        
        conn.commit()
        print("Successfully migrated postgres database!")
except Exception as e:
    print(f"Error migrating: {e}")

