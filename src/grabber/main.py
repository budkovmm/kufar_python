import asyncio
import json

from asyncpg.pool import Pool

from src.db.db import get_pool
from src.grabber.model import insert_ad
from src.grabber.http_client import HTTPClient
from src.grabber.dataclass import Ad, Pagination


def get_next_page_cursor(pagination: "Pagination"):
    for page in pagination.pages:
        if page.label == "next":
            return page.token
    return False


async def main():
    db_pool = await get_pool()
    await handle_page(db_pool=db_pool)


async def handle_page(db_pool: Pool, token=None):
    response = HTTPClient.get_ads(search_phrase="iphone", token=token).json()
    pagination = Pagination.from_dict(response["pagination"])
    next_page_token = get_next_page_cursor(pagination)
    if next_page_token:
        coros = [
            insert_ad(db_pool=db_pool, ad=Ad.from_dict(ad), row=json.dumps(ad))
            for ad in response["ads"]
        ]
        await asyncio.gather(*coros)
        await handle_page(db_pool=db_pool, token=next_page_token)
    else:
        print(response["total"])


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
