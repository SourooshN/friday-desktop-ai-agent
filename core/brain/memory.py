import os
import sys
import sqlite3
from datetime import datetime

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller onefile.
    """
    # PyInstaller bundles resources into a temp folder at sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# Path *inside* the bundle
DB_FILENAME = 'friday_memory.db'
DB_PATH = resource_path(DB_FILENAME)

def init_db():
    # Ensure the folder for DB exists when running unpacked
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.isdir(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    # If DB file doesn’t exist (first run), it will be created by sqlite
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            command TEXT,
            model TEXT,
            response TEXT
        );
    """)
    conn.commit()
    conn.close()

# Initialize on import
init_db()

def log_interaction(category: str, command: str, model: str, response: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO interactions (timestamp, category, command, model, response) VALUES (?, ?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), category, command, model, response)
    )
    conn.commit()
    conn.close()

def fetch_recent(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT * FROM interactions ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
