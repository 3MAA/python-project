import sqlite3
import os
from datetime import datetime
from app.models import OperationResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath("operations.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
            input_data TEXT NOT NULL,
            arg1 INTEGER,
            arg2 INTEGER,
            status TEXT DEFAULT 'pending',
            result TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def enqueue_task(operation: str, input_data: str, arg1: int, arg2: int | None = None) -> int:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO task_queue (operation, input_data, arg1, arg2, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (operation, input_data, arg1, arg2))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return task_id

def fetch_pending_tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, operation, input_data, arg1, arg2 FROM task_queue
        WHERE status = 'pending'
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def mark_task_done(task_id: int, result: str):
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE task_queue
        SET status = 'done', result = ?, timestamp = ?
        WHERE id = ?
    """, (result, timestamp, task_id))
    conn.commit()
    conn.close()

def mark_task_error(task_id: int, message: str):
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE task_queue
        SET status = 'error', result = ?, timestamp = ?
        WHERE id = ?
    """, (message, timestamp, task_id))
    conn.commit()
    conn.close()

def get_cached_result(operation: str, input_data: str) -> OperationResponse | None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT operation, input_data, result, timestamp FROM operations "
        "WHERE operation = ? AND input_data = ? ORDER BY timestamp DESC LIMIT 1",
        (operation, input_data)
    )
    row = c.fetchone()
    conn.close()
    if row:
        return OperationResponse(
            operation=row[0],
            input_data=row[1],
            result=row[2],
            timestamp=datetime.fromisoformat(row[3])
        )
    return None

def save_operation(operation: str, input_data: str, result: str) -> OperationResponse:
    timestamp = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO operations (operation, input_data, result, timestamp) VALUES (?, ?, ?, ?)",
        (operation, input_data, result, timestamp)
    )
    conn.commit()
    conn.close()
    return OperationResponse(
        operation=operation,
        input_data=input_data,
        result=result,
        timestamp=datetime.fromisoformat(timestamp)
    )

def fetch_all_operations() -> list[OperationResponse]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT operation, input_data, result, timestamp FROM operations ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return [
        OperationResponse(
            operation=row[0], input_data=row[1], result=row[2], timestamp=datetime.fromisoformat(row[3])
        )
        for row in rows
    ]

init_db()