from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "products" (
    "id" VARCHAR(26) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "price" INT NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "shop_id" VARCHAR(26) NOT NULL REFERENCES "shops" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_products_name_625ba0" ON "products" ("name");
COMMENT ON TABLE "products" IS 'Model to represent products.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "products";"""
