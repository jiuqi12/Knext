from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(11) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(16) NOT NULL COMMENT '密码',
    `is_active` BOOL NOT NULL COMMENT '账号是否可用' DEFAULT 1
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlW1vmzAQx79KxKtO6iYggUR7l0Sb1qlNpK6ZJjUVMmCIFWNT2/RBVb77bBPCQ0JKp1"
    "Vdpb2D/93Zdz+OuycjoSHE/NOCQ2Z87j0ZBCRQPtT0054B0rRUlSCAj7VjVnj4XDAQCKlF"
    "AHMopRDygKFUIEqkSjKMlUgD6YhIXEoZQbcZ9ASNoVjpPK5vpIxICB8gL17TtRchiMNami"
    "hUd2vdE4+p1s6I+Kod1W2+F1CcJaR0Th/FipKdNyJCqTEkkAEB1fGCZSp9ld22yqKiPNPS"
    "JU+xEhPCCGRYVMrtyCCgRPGT2XBdYKxu+Whbg+Fg1HcHI+miM9kpw01eXll7HqgJzK6Mjb"
    "YDAXIPjbHkpr6aft6jN10BdhhfNaYBUabehFggewWKxjIbOvZombl2f7jMnIGZJ/s81QQ8"
    "eBiSWKzkq2UdQfhzfDn9Nr48sawP6mwqWzvv99nWYmuTolxSTQHn95Qd6Ml2qtWYv0O1EE"
    "qs5Q/5HFfHD1xJd2Raf0TU7ULUbSfqNoki7smZgu4ONOqEUgwBafnVq3ENrL4MfC2uuwZu"
    "cB2FtuTq9CPZr65rR6prcwVGeTd3432E72Q+P1eHJJzfYi2cXTVALy4mX+QH0PylExKwnB"
    "ZqxEbryrBQgg+C9T1gobdnoTZt8903JXbSVAABsWao6lRVbRfOGDIUrA6toq3l6DICpc//"
    "dfSO1tEdZFyl9IK5WQl547HZnWJtWNqO02FaSq/Wcalt9Xmpfo0XQNy6v0+Alml2WTem2b"
    "5vlK0OUN4oYP4P1iF+/zGfHYZYCWmAXBBZ4HWIAnHaw4iLm38T6xGKquraUingnVyMfzW5"
    "Ts/nE02BchEzfYo+YPLW62XzGy5nGPQ="
)
