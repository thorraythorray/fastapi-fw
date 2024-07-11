from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `admin_role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_tm` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `update_tm` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(32) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `admin_user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_tm` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `update_tm` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `name` VARCHAR(64) NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `phone` VARCHAR(16),
    `age` INT,
    `sex` SMALLINT NOT NULL  COMMENT 'UNKOWN: 0\nMALE: 1\nFEMALE: 2' DEFAULT 0,
    `avatar` VARCHAR(255),
    `is_active` BOOL NOT NULL  DEFAULT 1,
    `role_id` INT,
    CONSTRAINT `fk_admin_us_admin_ro_7193bd4b` FOREIGN KEY (`role_id`) REFERENCES `admin_role` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
