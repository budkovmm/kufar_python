"""
Create ads table
"""

from yoyo import step, group

__depends__ = {}

group(
    [
        step(
            """
            create table ads (
                id        serial not null constraint ads_pk primary key,
                kufar_id  integer   not null,
                title     char(100) not null,
                link      char(50),
                json      jsonb,
                price_usd money not null
            )
         """,
            "DROP TABLE ads",
        ),
        step(
            "create unique index ads_id_uindex on ads (id)", "DROP INDEX ads_id_uindex"
        ),
        step(
            "create unique index ads_kufar_id_uindex on ads (kufar_id)",
            "DROP INDEX ads_kufar_id_uindex",
        ),
    ]
)
