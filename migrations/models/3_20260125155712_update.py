from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(118) NOT NULL COMMENT '密码';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(16) NOT NULL COMMENT '密码';"""


MODELS_STATE = (
    "eJztlm1vmzAQx79KlVed1E08xIHuXVpp2qatlbp1mtRUyMBBrIKh2PRBVb77fCYJkEJKq0"
    "5Zpb1B8L87c/fjfPhhlGYhJOLDuYBi9HHvYcRpCuqmpR/sjWie1yoKkvqJdixXHr6QBQ2k"
    "0iKaCFBSCCIoWC5ZxpXKyyRBMQuUI+NxLZWcXZfgySwGOdd5XFwqmfEQ7kCsHvMrL2KQhK"
    "00WYjv1ron73OtfeHyk3bEt/lekCVlymvn/F7OM772ZlyiGgOHgkrA5WVRYvqY3bLKVUVV"
    "prVLlWIjJoSIlolslDuQQZBx5KeyEbrAGN/y3jLHzti1J2NXuehM1oqzqMqra68CNYGTn6"
    "OFtlNJKw+NseaGX03fP6J3PKdFN75mzAZElfomxBWyv0BxNCsdYrmzcmLZzqwkY6NK9mmq"
    "Kb3zEuCxnKtH09yC8Nf07Pjz9GzfNN/h2plq7arfT5YWS5uQck01p0LcZkVHT/ZTbca8Dt"
    "WVUGOtN+RTXIkfTBRd1zBfRtQdhNTdwtTdhMqEp8YKu+no1f6d3ox5esO/FlW7C6kbWgop"
    "sSPVqs7E8dV9RIhqXt8y1ZU4xqyMIiNQumWG6noYoI9tqqgx2NRemyNioyF0K4OB0ZH2Mj"
    "DOhqjaGAM/3auMmPo7QUpZ8pzOXwfsvu0PDQqKne+/qO0ta0DXW1Zv06OpzTKEnBYyhapV"
    "hwJtR+2eKgkIYHe6gIRBte0hgaHd2R4s9pC5YvePFRsJ4ykiumr8D1HwaXB1S4vQe2TJrK"
    "zP97EptdJNhXIaa2JYIea/PFNNoWDBvOu0tbRsPW/R2uf/iesNnbhuoBCY0jP2cyNkx5t5"
    "OMX2YCRkyGQkpH80oq09G3FrPAPi0v1tAjQNY8jgM4z+yYe2NkD1Rtn5Z/n64/SkG2IjZA"
    "PkOVcFXoQskAd7CRPy8t/EuoUiVo1Jp0JcJ014+9+nvze5Hn87PdIUMiHjQq+iFzja9e9l"
    "8QeFOgE0"
)
