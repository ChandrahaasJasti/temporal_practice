import asyncio

async def cr1():
    print("cr1 started")
    await asyncio.sleep(2)
    print("cr1")

async def cr2():
    print("cr2 started")
    await asyncio.sleep(1)
    print("cr2")


async def main():
    print("main started")
    task1=asyncio.create_task(cr1())
    task2=asyncio.create_task(cr2())
    await task1
    print("task1 completed")
    await task2
    print("task2 completed")
    print("main completed")

asyncio.run(main())