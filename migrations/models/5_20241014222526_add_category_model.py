from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" VARCHAR(26) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(200) NOT NULL,
    "slug" VARCHAR(200) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_categories_title_66c3bc" ON "categories" ("title");
CREATE INDEX IF NOT EXISTS "idx_categories_slug_3a37a8" ON "categories" ("slug");
COMMENT ON TABLE "categories" IS 'Model to represent categories.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "categories";"""
