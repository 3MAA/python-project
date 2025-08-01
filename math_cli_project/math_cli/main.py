import click
from math_cli.controller import (
    handle_pow, handle_fib, handle_factorial,
    submit_pow, submit_fib, submit_factorial,
    show_history
)

@click.group()
def cli():
    """CLI pentru operatii matematice (pow, fib, factorial)."""
    pass

@cli.command()
@click.argument('base', type=int)
@click.argument('exp', type=int)
def pow(base, exp):
    handle_pow(base, exp)

@cli.command()
@click.argument('n', type=int)
def fib(n):
    handle_fib(n)

@cli.command()
@click.argument('n', type=int)
def factorial(n):
    handle_factorial(n)

@cli.command(name="submit-pow")
@click.argument('base', type=int)
@click.argument('exp', type=int)
def submit_pow_cmd(base, exp):
    submit_pow(base, exp)

@cli.command(name="submit-fib")
@click.argument('n', type=int)
def submit_fib_cmd(n):
    submit_fib(n)

@cli.command(name="submit-factorial")
@click.argument('n', type=int)
def submit_factorial_cmd(n):
    submit_factorial(n)

@cli.command()
def history():
    show_history()

if __name__ == '__main__':
    cli()
