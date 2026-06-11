import os
from dotenv import load_dotenv
load_dotenv()
from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        res = conn.execute(text("SELECT 1")).scalar()
        if res == 1:
            print("SUCCESS! Database is fully reachable.")
except Exception as e:
    print("FAILED:", e)
