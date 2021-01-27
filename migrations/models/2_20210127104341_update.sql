-- upgrade --
ALTER TABLE `daily_basket_list` MODIFY COLUMN `basket_list` LONGTEXT;
-- downgrade --
ALTER TABLE `daily_basket_list` MODIFY COLUMN `basket_list` LONGTEXT;
