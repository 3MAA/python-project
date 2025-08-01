from math import factorial as math_factorial

def calculate_pow(base: int, exp: int) -> int:
    return base ** exp

def calculate_fib(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci nu e definit pentru n negativ")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def calculate_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorialul nu e definit pentru n negativ")
    return math_factorial(n)
