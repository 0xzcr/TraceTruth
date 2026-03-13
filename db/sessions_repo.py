import time
from db.connection import get_connection


def create_session(session_id, user_id, device=None, app_version=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (session_id, user_id, start_time, device, app_version) VALUES (?, ?, ?, ?, ?)",
            (session_id, user_id, time.time(), device, app_version),
        )
        conn.commit()


def end_session(session_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET end_time = ? WHERE session_id = ?",
            (time.time(), session_id),
        )
        conn.commit()


def list_sessions_for_student(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, start_time, end_time FROM sessions WHERE user_id = ? ORDER BY start_time DESC",
            (user_id,),
        )
        return cursor.fetchall()


def list_all_sessions_with_users():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.session_id, s.start_time, s.end_time, u.username
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.start_time DESC
            """
        )
        return cursor.fetchall()
