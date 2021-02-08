-- upgrade --
ALTER TABLE `account_setting` ADD `use_smaregi_webhook` BOOL NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE `account_setting` DROP COLUMN `use_smaregi_webhook`;
