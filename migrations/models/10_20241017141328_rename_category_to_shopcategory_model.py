from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """ALTER TABLE categories RENAME TO shop_categories;"""

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """ALTER TABLE shop_categories RENAME TO categories;"""
