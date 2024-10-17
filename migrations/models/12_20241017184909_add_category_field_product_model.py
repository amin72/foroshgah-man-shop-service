from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "products" ADD "category_id" VARCHAR(26);
        ALTER TABLE "products" ADD CONSTRAINT "fk_products_product__a7f77cf2" FOREIGN KEY ("category_id") REFERENCES "product_categories" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "products" DROP CONSTRAINT "fk_products_product__a7f77cf2";
        ALTER TABLE "products" DROP COLUMN "category_id";"""
