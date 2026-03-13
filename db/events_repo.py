import time
from db.connection import get_connection


def log_event(session_id, event_type, content=None, cursor_pos=None, selection_start=None, selection_end=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (session_id, timestamp, event_type, content, cursor_pos, selection_start, selection_end)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, time.time(), event_type, content, cursor_pos, selection_start, selection_end),
        )
        conn.commit()


def list_events(session_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, event_type, content, cursor_pos, selection_start, selection_end FROM events WHERE session_id = ? ORDER BY id",
            (session_id,),
        )
        return cursor.fetchall()
