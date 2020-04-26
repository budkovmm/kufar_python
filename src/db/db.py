import asyncpg
from asyncpg.pool import Pool

KUFAR = "kufar"


async def get_pool() -> Pool:
    pool = await asyncpg.create_pool(
        user=KUFAR, database=KUFAR, password=KUFAR, command_timeout=60
    )
    return pool
