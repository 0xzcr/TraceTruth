import os
import sqlite3
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "events.db")


def get_connection():
    return sqlite3.connect(DB_PATH)

#funct - create schema 
def create_schema():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                content TEXT
            )
            """
        )
        conn.commit()


def log_event(event_type, content):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (timestamp, event_type, content) VALUES (?, ?, ?)",
            (time.time(), event_type, content),
        )
        conn.commit()
