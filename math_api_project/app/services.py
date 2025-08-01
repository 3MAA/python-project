from datetime import datetime

from fastapi import HTTPException

from app.database import (
    get_cached_result,
    save_operation,
    fetch_all_operations
)
from app.models import OperationResponse
from math import factorial as math_factorial

def calculate_pow(base: int, exp: int) -> int:
    return base ** exp

def calculate_fib(n: int) -> int:
    if n < 0:
        raise HTTPException(status_code=400, detail="Fibonacci not defined for negative numbers!")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def calculate_factorial(n: int) -> int:
    if n < 0:
        raise HTTPException(status_code=400, detail="Factorial not defined for negative numbers!")
    return math_factorial(n)

def handle_pow(base: int, exp: int) -> OperationResponse:
    input_data = f"base={base}, exp={exp}"
    cached = get_cached_result("pow", input_data)
    if cached:
        return cached
    result = calculate_pow(base, exp)
    return save_operation("pow", input_data, str(result))

def handle_fib(n: int) -> OperationResponse:
    input_data = f"n={n}"
    cached = get_cached_result("fib", input_data)
    if cached:
        return cached
    result = calculate_fib(n)
    return save_operation("fib", input_data, str(result))

def handle_factorial(n: int) -> OperationResponse:
    input_data = f"n={n}"
    cached = get_cached_result("factorial", input_data)
    if cached:
        return cached
    result = calculate_factorial(n)
    return save_operation("factorial", input_data, str(result))

def get_history() -> list[OperationResponse]:
    return fetch_all_operations()
