import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database/events.db")

conn = sqlite3.connect("DB_PATH")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL,
    event_type TEXT,
    content TEXT
)
""")

conn.commit()


def log_event(event_type, content):
    cursor.execute(
        "INSERT INTO events (timestamp, event_type, content) VALUES (strftime('%s','now'), ?, ?)",
        (event_type, content)
    )
    conn.commit()