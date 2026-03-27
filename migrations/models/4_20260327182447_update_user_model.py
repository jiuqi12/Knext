from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `last_login_attempt` DATETIME(6) COMMENT '最后登录尝试时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` ADD `login_attempts` INT NOT NULL COMMENT '登录错误次数，超过三次禁用账号' DEFAULT 0;
        ALTER TABLE `user` CHANGE password hash_password VARCHAR(118);
        ALTER TABLE `user` ADD `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` DROP COLUMN `department`;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(30) NOT NULL COMMENT '邮箱';
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(30) NOT NULL COMMENT '用户名';
        ALTER TABLE `user` ALTER COLUMN `is_active` SET DEFAULT 1;
        ALTER TABLE `user` MODIFY COLUMN `is_active` BOOL NOT NULL COMMENT '激活状态' DEFAULT 1;
        ALTER TABLE `user` MODIFY COLUMN `is_active` BOOL NOT NULL COMMENT '激活状态' DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` CHANGE hash_password password VARCHAR(118);
        ALTER TABLE `user` ADD `department` VARCHAR(13) NOT NULL COMMENT '属于部门';
        ALTER TABLE `user` DROP COLUMN `last_login_attempt`;
        ALTER TABLE `user` DROP COLUMN `login_attempts`;
        ALTER TABLE `user` DROP COLUMN `created_at`;
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(22) NOT NULL COMMENT '邮箱';
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(11) NOT NULL COMMENT '用户名';
        ALTER TABLE `user` MODIFY COLUMN `is_active` INT NOT NULL COMMENT '账号登录次数，初始化为3，当变为0时不可用' DEFAULT 3;
        ALTER TABLE `user` ALTER COLUMN `is_active` SET DEFAULT 3;
        ALTER TABLE `user` MODIFY COLUMN `is_active` INT NOT NULL COMMENT '账号登录次数，初始化为3，当变为0时不可用' DEFAULT 3;"""


MODELS_STATE = (
    "eJztl21P2zAQx79K1VdMYihJm4fuXQudYAI6QdkmKIqcxGktErvEDlAhvvvObtM06TMqg2"
    "l7EyV/3znnn+07+7kaswBH/OCK46T6pfJcpSjG8FLQ9ytVNBzmqhQE8iJlmGYWHhcJ8gVo"
    "IYo4BinA3E/IUBBGQaVpFEmR+WBIaD+XUkruU+wK1sdioOK4uQWZ0AA/YZ59Du/ckOAoKI"
    "RJAvlvpbtiNFTaCRVflaH8m+f6LEpjmhsPR2LA6NSaUCHVPqY4QQLL7kWSyvBldJNRZiMa"
    "R5qbjEOc8QlwiNJIzAx3QwY+o5IfRMPVAPvyL58NvW7XnZpVd8BERTJV7Jfx8PKxjx0Vgf"
    "Nu9UW1I4HGFgpjzk3Omnqfo3c4QMlifLM+JYgQehlihuwNKFZ7qW0aTi+1jJrdS826Ng52"
    "PdUYPbkRpn0xgM+atgLhj+bF4XHzYq+mfZJ9M1ja4/V+PmkxVJOknFMdID5wh4jzR5YsWJ"
    "jL0c457oZvJuSA8625jrDp+RZwdjT9NWx13dkALlgtpavaingJdyHBkIcFq7bFWIQRXbLv"
    "Z/1KZD1wfCu009VcQmuFvgbPoOYBYMMDzJa2KeYVVFudzqnsJOb8PlLCSbdE9+qs1QbsCj"
    "oYEYFn00VOOmJ9Ql0kBI6Hgm+RYucd16fbXeHWFiYKywbKZmiavbRh6o1e6ng4BOKeocPT"
    "tGEmwlDzQQ8csHFCH1JKHWuNzMZuOHqWcJzAgNkya6G94abYSRrP5wXHiETbJJapw/snlI"
    "aGMHD0vFcllN0naz/BcuSwWOeBHkGLIDFeDLXoWSIbTFwPspc/nrgNXa54sJPrO7Tkug/r"
    "GzKHkQUdGo0m2WsF8+7JWfuy2zz7Xkg5R81uW7YYSh2V1D2rND/TTio/T7rHFflZue6ctx"
    "VXxkU/UX/M7brXVRkTSgVzKXt0UTBzbMjUDFcxpSEu3EJ62nbaF/ewg+mfhL+T2bdsTVNH"
    "IlzMfaavBzL3BeY/vCpU8PIuEd7NnIql4CH/7hElgTvXwgy2zHa+KTbisoIo6qs5lGxllJ"
    "ObVRMnxB9UF9y5Ji37q25dKLf5f+9avzE+zL3rASdchrRFCZ9xeecivjnFQuk2THOD2g1W"
    "S4u3aitWb7k1toA4Mf87AeraJocfsFp+mdLmjz+MCkwXFMFvl53zJeee3KUE8orCAG8C4o"
    "v9SkS4uP2YWFdQlKMu1KwM3t5Z81eZ6+Fpp1UuRrKDFjB+1/Ly8hsdNktU"
)
