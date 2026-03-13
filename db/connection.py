import os
import sqlite3
from utils.paths import DB_DIR, DB_PATH


def ensure_db_dir():
    os.makedirs(DB_DIR, exist_ok=True)


def get_connection():
    ensure_db_dir()
    return sqlite3.connect(DB_PATH)
