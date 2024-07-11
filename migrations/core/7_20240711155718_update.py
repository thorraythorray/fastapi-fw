from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `admin_user` ALTER COLUMN `sex` DROP DEFAULT;
        ALTER TABLE `admin_user` MODIFY COLUMN `sex` VARCHAR(2) NOT NULL  COMMENT 'unkown: 不明\nmale: 男性\nfemale: 女性';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `admin_user` MODIFY COLUMN `sex` SMALLINT NOT NULL  COMMENT 'unkown: 0\nmale: 1\nfemale: 2' DEFAULT 0;
        ALTER TABLE `admin_user` ALTER COLUMN `sex` SET DEFAULT 0;"""
