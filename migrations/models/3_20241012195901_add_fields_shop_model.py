from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shops" ADD "address" VARCHAR(1000);
        ALTER TABLE "shops" ADD "mobile" VARCHAR(11);
        ALTER TABLE "shops" ADD "description" VARCHAR(1000);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shops" DROP COLUMN "address";
        ALTER TABLE "shops" DROP COLUMN "mobile";
        ALTER TABLE "shops" DROP COLUMN "description";"""
