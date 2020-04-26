from typing import Type

from asyncpg import Connection

from src.grabber.dataclass import Ad


async def insert_ad(con: Connection, ad: "Ad", row):
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
