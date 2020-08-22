"""
This module contains initial experimentation code with the Python
async mechanics.
"""
from time import sleep
import asyncio


async def async_count():
    print("Entering async count")
    for k in range(10):
        print("Async sleeping")
        await asyncio.sleep(1)

    print("Exiting async count")

async def count():
    print("Entering count")
    for k in range(10):
        print("sleeping")
        sleep(1)
    print("Exiting count")


async def main():
    await asyncio.gather(async_count(), async_count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
