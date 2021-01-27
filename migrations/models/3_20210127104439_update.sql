-- upgrade --
CREATE TABLE IF NOT EXISTS `products` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `contract_id` VARCHAR(32) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `modified_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `product_id` INT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `color` VARCHAR(64),
    `size` VARCHAR(64),
    `image` VARCHAR(511),
    `price` INT,
    `category_id` INT,
    `group_code_id` VARCHAR(255)
) CHARACTER SET utf8mb4 COMMENT='商品モデル';
-- downgrade --
DROP TABLE IF EXISTS `products`;
