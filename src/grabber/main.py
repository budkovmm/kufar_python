import asyncio

from src.db.db import get_pool
from src.grabber.model import insert_ad
from src.helpers import round_price
from src.grabber.http_client import HTTPClient
from src.grabber.dataclass import SearchResultModel, Currency


async def main():
    response = HTTPClient.get_ads(search_phrase="iphone")
    search_result = SearchResultModel.from_http_response(response)
    db_pool = await get_pool()
    connection = await db_pool.acquire()
    row = str(response.content.decode("utf8"))
    for ad in search_result.ads:
        print("=======")
        print(ad.ad_id)
        print(ad.category)
        print(ad.subject)
        print(round_price(ad.price_byn), Currency.BYN.value)
        print(round_price(ad.price_usd), Currency.USD.value)
        print("=======")
        await insert_ad(connection, ad=ad, row=row)
    await db_pool.release(connection=connection)
    print(search_result.total)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
