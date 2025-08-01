import time
from app.database import (
    fetch_pending_tasks,
    get_cached_result,
    save_operation,
    mark_task_done,
    mark_task_error
)
from app.services import calculate_pow, calculate_fib, calculate_factorial

print("[Worker] Started processing task queue...")

while True:
    tasks = fetch_pending_tasks()
    if not tasks:
        time.sleep(1)
        continue

    for task_id, operation, input_data, arg1, arg2 in tasks:
        try:
            cached = get_cached_result(operation, input_data)
            if cached:
                print(f"[Worker] Task {task_id} already cached: {cached.result}")
                mark_task_done(task_id, cached.result)
                continue

            if operation == "pow":
                result = calculate_pow(arg1, arg2)
            elif operation == "fib":
                result = calculate_fib(arg1)
            elif operation == "factorial":
                result = calculate_factorial(arg1)
            else:
                raise ValueError(f"Unknown operation: {operation}")

            save_operation(operation, input_data, str(result))
            mark_task_done(task_id, str(result))
            print(f"[Worker] Task {task_id} processed: {operation}({input_data}) = {result}")

        except Exception as e:
            mark_task_error(task_id, str(e))
            print(f"[Worker] Task {task_id} failed: {e}")