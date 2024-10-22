from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "product_categories" (
    "id" VARCHAR(26) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(200) NOT NULL,
    "slug" VARCHAR(200) NOT NULL,
    "image" VARCHAR(255),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "shop_category_id" VARCHAR(26) REFERENCES "shop_categories" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_product_cat_title_e13750" ON "product_categories" ("title");
CREATE INDEX IF NOT EXISTS "idx_product_cat_slug_2cc100" ON "product_categories" ("slug");
COMMENT ON TABLE "product_categories" IS 'Model to represent product-categories.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "product_categories";"""
