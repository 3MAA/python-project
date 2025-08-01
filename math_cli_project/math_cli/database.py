import sqlite3
import os
from math_cli.models import OperationRequest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "../operations.db")

def operation_exists(operation: str, input_data: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM operations
        WHERE operation = ? AND input_data = ?
    """, (operation, input_data))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            input_data TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS task_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            arg1 INTEGER,
            arg2 INTEGER,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def save_operation(req: OperationRequest):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO operations (operation, input_data, result, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (req.operation, req.input_data, req.result, req.timestamp.isoformat()))
    conn.commit()
    conn.close()

def fetch_all_operations():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM operations ORDER BY timestamp DESC")
    results = c.fetchall()
    conn.close()
    return results

def enqueue_task(operation: str, arg1: int, arg2: int = None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO task_queue (operation, arg1, arg2, status)
        VALUES (?, ?, ?, 'pending')
    """, (operation, arg1, arg2))
    conn.commit()
    conn.close()

def fetch_pending_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT id, operation, arg1, arg2 FROM task_queue
        WHERE status = 'pending'
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def mark_task_processed(task_id: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE task_queue SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_cached_result(operation: str, input_data: str) -> str | None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT result FROM operations
        WHERE operation = ? AND input_data = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (operation, input_data))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

init_db()
