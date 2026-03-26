from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ALTER COLUMN `is_active` SET DEFAULT 3;
        ALTER TABLE `user` MODIFY COLUMN `is_active` INT NOT NULL COMMENT '账号登录次数，初始化为3，当变为0时不可用' DEFAULT 3;
        ALTER TABLE `user` MODIFY COLUMN `is_active` INT NOT NULL COMMENT '账号登录次数，初始化为3，当变为0时不可用' DEFAULT 3;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `is_active` BOOL NOT NULL COMMENT '账号是否可用' DEFAULT 1;
        ALTER TABLE `user` ALTER COLUMN `is_active` SET DEFAULT 1;
        ALTER TABLE `user` MODIFY COLUMN `is_active` BOOL NOT NULL COMMENT '账号是否可用' DEFAULT 1;"""


MODELS_STATE = (
    "eJztlW1r2zAQx79K8asOuuGH+GF7lwbGNrYUunUMmmJkW3ZEbMm15D5Q8t2nk5P4IU7ijo"
    "yusDfG/t+ddPezdPekZSzCKX93xXGhfTh50ijKsHxp6WcnGsrzWgVBoCBVjuXaI+CiQKGQ"
    "WoxSjqUUYR4WJBeEUanSMk1BZKF0JDSppZKS2xL7giVYzFUe1zdSJjTCD5ivP/OFHxOcRq"
    "00SQR7K90Xj7nSPlPxUTnCboEfsrTMaO2cP4o5oxtvQgWoCaa4QALD8qIoIX3IblXluqIq"
    "09qlSrERE+EYlalolDuQQcgo8JPZcFVgAru8NY2RO/IsZ+RJF5XJRnGXVXl17VWgIjD9oS"
    "2VHQlUeSiMNTf4a+p9i95kjop+fM2YDkSZehfiGtlfoKjNStc2vVnpmJY7K+2RXiV7mGqG"
    "HvwU00TM5adh7EH4c3w5+TS+PDWMN7A2k0e7Ou/TlcVUJqBcU80R5/es6DmTu6k2Y45DdS"
    "3UWOsLeYirHYSOpOvpxh8RdYYQdXYTdbpECfdlTyF3PQd19zVvxhy+7cdCavXx9CJT8rSt"
    "WJ5T13ED+R7btjy5gWnIp+3qszKO9VDqphHJ5/sQfCxDRo2whayNObYtMEReZdAhOlZeOs"
    "RZOK5uxcD/doT+Ak05XjTaCwgBChf3qIj8LQsz2S7fbVNmZl0FUZQo9FARJLcaUWNckHDe"
    "N7xWlr3jC9U+/wfYKxpgd7jgkNIzOm0j5IUb7XCKrfZq2vaA/iq9djZYZWt3WLgaz4C4cn"
    "+dAA1dHzKgdH33hAJbG6DcUeDqDrYhfvl+Me2H2AjpgLyissDriITi7CQlXNz8m1j3UISq"
    "IemM89u0Ce/02/hXl+vk68W5osC4SAq1ilrg/KXHy/I3mPcnHA=="
)
