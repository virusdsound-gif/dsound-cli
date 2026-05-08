import asyncio

async def run_task(name, coro):
    print(f"Running {name}")
    await coro

async def orchestrate(tasks):
    await asyncio.gather(*tasks)
