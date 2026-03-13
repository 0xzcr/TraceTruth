import time
from db.connection import get_connection


def create_document(doc_id, session_id, title=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO documents (doc_id, session_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (doc_id, session_id, title, time.time(), time.time()),
        )
        conn.commit()


def update_document_text(doc_id, text):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE documents SET final_text = ?, updated_at = ? WHERE doc_id = ?",
            (text, time.time(), doc_id),
        )
        conn.commit()


def get_document_by_session(session_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT doc_id, title, final_text FROM documents WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {"doc_id": row[0], "title": row[1], "final_text": row[2]}
