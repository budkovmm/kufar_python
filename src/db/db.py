import asyncpg
from asyncpg.pool import Pool

from src.constants import KUFAR


async def get_pool() -> Pool:
    pool = await asyncpg.create_pool(
        user=KUFAR, database=KUFAR, password=KUFAR, command_timeout=60
    )
    return pool
