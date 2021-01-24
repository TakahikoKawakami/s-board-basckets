-- upgrade --
ALTER TABLE `accounts` MODIFY COLUMN `access_token` VARCHAR(1024) NOT NULL;
-- downgrade --
ALTER TABLE `accounts` MODIFY COLUMN `access_token` VARCHAR(128) NOT NULL;
