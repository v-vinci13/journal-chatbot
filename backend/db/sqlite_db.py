import sqlite3

DB_NAME = "journal.db"


# -----------------------
# INIT DB (run once at startup)
# -----------------------
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        content TEXT,
        sentiment TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -----------------------
# SAFE MIGRATION (ADD sentiment if missing)
# -----------------------
def migrate_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(entries)")
    columns = [col[1] for col in cursor.fetchall()]

    if "sentiment" not in columns:
        cursor.execute("ALTER TABLE entries ADD COLUMN sentiment TEXT")

        
    conn.commit()
    conn.close()


# -----------------------
# SAVE ENTRY
# -----------------------
def save_entry(user_id, content, sentiment):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO entries (user_id, content, sentiment) VALUES (?, ?, ?)",
        (user_id, content, sentiment)
    )

    conn.commit()
    conn.close()


# -----------------------
# GET ENTRIES (with sentiment)
# -----------------------
def get_entries(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, content, sentiment FROM entries WHERE user_id=?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "content": row[1], "sentiment": row[2]}
        for row in rows
    ]


# -----------------------
# GET ALL ENTRIES (content only)
# -----------------------
def get_all_entries(user_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM entries WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


# -----------------------
# GET RECENT ENTRIES (for weekly reflection)
# -----------------------
def get_recent_entries(user_id, limit=20):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM entries WHERE user_id=? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )

    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]

def delete_entry(entry_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM entries WHERE id=?", (entry_id,))

    conn.commit()
    conn.close()

def clear_all(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM entries WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()    