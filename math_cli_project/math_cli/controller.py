from math_cli.services import calculate_pow, calculate_fib, calculate_factorial
from math_cli.database import (
    save_operation, fetch_all_operations,
    enqueue_task
)
from math_cli.models import OperationRequest
from datetime import datetime

def handle_pow(base: int, exp: int):
    result = calculate_pow(base, exp)
    print(f"Rezultat: {result}")
    req = OperationRequest(
        operation="pow",
        input_data=f"base={base}, exp={exp}",
        result=str(result)
    )
    save_operation(req)

def handle_fib(n: int):
    result = calculate_fib(n)
    print(f"Rezultat: {result}")
    req = OperationRequest(
        operation="fib",
        input_data=f"n={n}",
        result=str(result)
    )
    save_operation(req)

def handle_factorial(n: int):
    result = calculate_factorial(n)
    print(f"Rezultat: {result}")
    req = OperationRequest(
        operation="factorial",
        input_data=f"n={n}",
        result=str(result)
    )
    save_operation(req)

def submit_pow(base: int, exp: int):
    enqueue_task("pow", base, exp)
    print(f"[CLI] Task 'pow' trimis în coadă: ({base}, {exp})")

def submit_fib(n: int):
    enqueue_task("fib", n)
    print(f"[CLI] Task 'fib' trimis în coadă: ({n},)")

def submit_factorial(n: int):
    enqueue_task("factorial", n)
    print(f"[CLI] Task 'factorial' trimis în coadă: ({n},)")

def show_history():
    ops = fetch_all_operations()
    print("\nIstoric operatii:")
    for row in ops:
        print(f"[{row[4]}] {row[1]}({row[2]}) = {row[3]}")
