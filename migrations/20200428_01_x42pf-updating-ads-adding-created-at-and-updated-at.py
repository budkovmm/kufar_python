"""
Updating ads, adding created_at and updated_at
"""

from yoyo import step

__depends__ = {"20200426_01_crHPi-create-ads-table"}

steps = [
    step(
        "alter table ads add created_at timestamp default now() not null",
        "alter table ads drop column created_at",
    ),
    step(
        "alter table ads add updated_at timestamp default now() not null",
        "alter table ads drop column updated_at",
    ),
]
