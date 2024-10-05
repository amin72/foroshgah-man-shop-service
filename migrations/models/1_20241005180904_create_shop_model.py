from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "shops" (
    "id" VARCHAR(26) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(200) NOT NULL,
    "owner_id" VARCHAR(26) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_shops_name_402c1a" ON "shops" ("name");
CREATE INDEX IF NOT EXISTS "idx_shops_owner_i_4b2434" ON "shops" ("owner_id");
COMMENT ON TABLE "shops" IS 'Model to represent shops.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "shops";"""
