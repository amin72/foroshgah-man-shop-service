from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shops" ADD "category_id" VARCHAR(26);
        ALTER TABLE "shops" ADD CONSTRAINT "fk_shops_categori_b1959cb6" FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shops" DROP CONSTRAINT "fk_shops_categori_b1959cb6";
        ALTER TABLE "shops" DROP COLUMN "category_id";"""
