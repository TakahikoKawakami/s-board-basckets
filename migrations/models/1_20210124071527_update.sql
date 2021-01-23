-- upgrade --
CREATE TABLE IF NOT EXISTS `accounts` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `contract_id` VARCHAR(32) NOT NULL,
    `created_at` DATETIME(6) NOT NULL,
    `modified_at` DATETIME(6) NOT NULL,
    `access_token` VARCHAR(128) NOT NULL,
    `expiration_date_time` DATETIME(6) NOT NULL,
    `status` VARCHAR(16) NOT NULL,
    `test` VARCHAR(32) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='アカウントモデル';
-- downgrade --
DROP TABLE IF EXISTS `accounts`;
