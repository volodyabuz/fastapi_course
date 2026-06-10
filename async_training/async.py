import asyncio
import time


# IO bound
async def make_db_call():
    await asyncio.sleep(1)

async def make_api_request():
    await asyncio.sleep(2)


async def main():
    start_time = time.perf_counter()
    await asyncio.gather(
        make_db_call(),
        make_api_request()
    )
    # await make_db_call()
    # await make_api_request()
    end_time = time.perf_counter()
    print("Времени прошло: ", end_time - start_time)


if __name__ == "__main__":
    asyncio.run(main())
