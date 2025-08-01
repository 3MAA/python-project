import asyncio
from math_cli.worker import worker

async def main():
    await worker()

if __name__ == '__main__':
    asyncio.run(main())
