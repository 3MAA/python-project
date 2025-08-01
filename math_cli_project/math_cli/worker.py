import time
from math_cli.services import calculate_pow, calculate_fib, calculate_factorial
from math_cli.models import OperationRequest
from math_cli.database import (
    fetch_pending_tasks,
    mark_task_processed,
    save_operation,
    operation_exists,
    get_cached_result
)
from datetime import datetime

print("[Worker] Pornit. Așteaptă taskuri...")

while True:
    tasks = fetch_pending_tasks()
    if not tasks:
        time.sleep(1)
        continue

    for task_id, op, arg1, arg2 in tasks:
        try:
            if op == "pow":
                input_data = f"base={arg1}, exp={arg2}"
                cached = get_cached_result(op, input_data)
                if cached:
                    print(f"[Worker] Rezultat din cache: {op}({input_data}) = {cached}")
                    mark_task_processed(task_id)
                    continue
                result = calculate_pow(arg1, arg2)

            elif op == "fib":
                input_data = f"n={arg1}"
                cached = get_cached_result(op, input_data)
                if cached:
                    print(f"[Worker] Rezultat din cache: {op}({input_data}) = {cached}")
                    mark_task_processed(task_id)
                    continue
                result = calculate_fib(arg1)

            elif op == "factorial":
                input_data = f"n={arg1}"
                cached = get_cached_result(op, input_data)
                if cached:
                    print(f"[Worker] Rezultat din cache: {op}({input_data}) = {cached}")
                    mark_task_processed(task_id)
                    continue
                result = calculate_factorial(arg1)

            else:
                raise ValueError(f"Operatie necunoscuta: {op}")

            req = OperationRequest(
                operation=op,
                input_data=input_data,
                result=str(result),
                timestamp=datetime.utcnow()
            )
            save_operation(req)
            mark_task_processed(task_id)
            print(f"[Worker] Procesat: {op}({input_data}) = {result}")

        except Exception as e:
            print(f"[Worker] Eroare la task #{task_id}: {e}")
            mark_task_processed(task_id)
