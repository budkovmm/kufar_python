from asyncpg.pool import Pool

from src.constants import Currency
from src.grabber.dataclass import Ad
from src.helpers import round_price


async def insert_ad(db_pool: Pool, ad: "Ad", row):
    con = await db_pool.acquire()
    print("=======")
    print(ad.ad_id)
    print(ad.category)
    print(ad.subject)
    print(round_price(ad.price_byn), Currency.BYN.value)
    print(round_price(ad.price_usd), Currency.USD.value)
    print("=======")
    await con.fetch(
        """
        INSERT INTO ads (kufar_id, title, link, json, price_usd)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (kufar_id)
        DO
        UPDATE SET title = EXCLUDED.title, link = EXCLUDED.link, json = EXCLUDED.json, price_usd = EXCLUDED.price_usd
    """,
        ad.ad_id,
        ad.subject,
        ad.ad_link,
        row,
        str(ad.price_usd),
    )
    await db_pool.release(connection=con)
