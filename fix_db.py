import sqlite3

def fix_db():
    conn = sqlite3.connect('exam.db')
    cursor = conn.cursor()

    # 1. Delete Fallback questions
    cursor.execute('DELETE FROM questions WHERE text LIKE "%Fallback%"')
    print(f'Deleted {cursor.rowcount} Fallback questions.')

    # 2. Migrate resources table
    cursor.execute('PRAGMA table_info(resources)')
    cols = {row[1] for row in cursor.fetchall()}

    migrations = {
        'exam_name': 'ALTER TABLE resources ADD COLUMN exam_name TEXT DEFAULT ""',
        'file_path': 'ALTER TABLE resources ADD COLUMN file_path TEXT DEFAULT ""',
        'file_name': 'ALTER TABLE resources ADD COLUMN file_name TEXT DEFAULT ""',
        'tags': 'ALTER TABLE resources ADD COLUMN tags TEXT DEFAULT ""',
        'uploaded_by': 'ALTER TABLE resources ADD COLUMN uploaded_by INTEGER',
    }

    for col, sql in migrations.items():
        if col not in cols:
            cursor.execute(sql)
            print(f'Added column {col} to resources table.')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_db()
