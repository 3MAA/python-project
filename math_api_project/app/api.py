from fastapi import APIRouter, HTTPException
from app.models import PowRequest, SingleIntRequest, OperationResponse
from app.database import enqueue_task, fetch_all_operations
from app.database import get_cached_result  # reused for polling

router = APIRouter()

@router.post("/pow")
def pow_route(req: PowRequest):
    input_data = f"base={req.base}, exp={req.exp}"
    task_id = enqueue_task("pow", input_data, req.base, req.exp)
    return {"message": "Task submitted", "task_id": task_id}

@router.post("/fib")
def fib_route(req: SingleIntRequest):
    input_data = f"n={req.n}"
    task_id = enqueue_task("fib", input_data, req.n)
    return {"message": "Task submitted", "task_id": task_id}

@router.post("/factorial")
def factorial_route(req: SingleIntRequest):
    input_data = f"n={req.n}"
    task_id = enqueue_task("factorial", input_data, req.n)
    return {"message": "Task submitted", "task_id": task_id}

@router.get("/history", response_model=list[OperationResponse])
def history_route():
    return fetch_all_operations()

@router.get("/result/{task_id}")
def get_task_result(task_id: int):
    import sqlite3, os
    DB_PATH = os.path.abspath("operations.db")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT status, result FROM task_queue
        WHERE id = ?
    """, (task_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Task ID not found")

    status, result = row
    return {"status": status, "result": result if status == "done" else None}
