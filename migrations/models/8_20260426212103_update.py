from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP FOREIGN KEY `fk_user_userrole_c8bc91ea`;
        ALTER TABLE `user` CHANGE role_id role INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` CHANGE role role_id INT;
        ALTER TABLE `user` ADD CONSTRAINT `fk_user_userrole_c8bc91ea` FOREIGN KEY (`role_id`) REFERENCES `userroles` (`id`) ON DELETE CASCADE;"""


MODELS_STATE = (
    "eJztmW1vozgQgP9KlE89qbcCEl5y35K2p+1p26y66d1pNytkwCRWwc5i02616n8/jwkhEP"
    "JCL21SqV9SGM/A+PF4ZnB/tWMW4Ih/uOU4af/R+tWmKMbyoiQ/bbXRbFZIQSCQFynFNNfw"
    "uEiQL6QsRBHHUhRg7idkJgijUkrTKAIh86UioZNClFLyI8WuYBMspsqPb9+lmNAA/8Q8v5"
    "3duSHBUVBykwTwbiV3xeNMyS6p+FMpwts812dRGtNCefYopowutAkVIJ1gihMkMDxeJCm4"
    "D97NZ5nPKPO0UMlcXLIJcIjSSCxNd0cGPqPAT3rD1QQn8JbfDb1rd52O1XWkivJkIbGfsu"
    "kVc88MFYHrUftJjSOBMg2FseAGq6auV+idTVFSj2/ZpgJRul6FmCN7AYrtcWqbhjNOLaNj"
    "j1Ozq2XObqcao59uhOlETOVtR9uA8O/+zdnH/s1JR/sNns1kaGfxfj0fMdQQUC6oThGfuj"
    "PE+QNLagJzPdoVw/3wzQUF4GJrbiNser4lOTua/hy2uu7sAFdqraWrxsp4CXdlgiH3NVE7"
    "YCzCiK7Z98t2FbKeNHwptItorqC1LCOEsDUs9Rsuwtns9MapEyh5J7R3A7+B82A4/AQPiT"
    "n/ESnB5ajC+/ZqcCEXQi2DVCICLyeQgn3EJoS6SAgczwRvkHRXDbcn4H0tgFabOizbk3xD"
    "0xynPVMH4h6Wa2B5hg5rYGvjNAw1H1bCkTpO6Msk08VaL9exe46er1nT1dpPYi/viSAm9B"
    "lbIjd7xR1R3xlUtkR2bXsIIHc1tUlM55g2QyLJNtgCufrrBf66pO70AkP+GrZxeX6YeMUx"
    "IlGT0rgwOHxJ7GkIQ2B6zyqJ+283/ATDzGVyXQV6LkcEiXE91LJlhWwwN/2QX7x662HokK"
    "GlHuTj0II8HXZ3ZC5nFgxp9DivvxuYjy6vLr6M+lefS1nhvD+6gBFDSR8r0hOrsj6Lh7T+"
    "uRx9bMFt6+vw+kJxZVxMEvXGQm/0tQ0+oVQwl7IHmYaXGt9cmuMql2DEhVsqp02Xvf4Je1"
    "j+uft7WX3L1jTV1ONyrTZ9PYBaHZjNo+KNREEOaSUM4Ps3vFv6kgOBh/y7B5QE7soIM9g6"
    "3dWh2IirEkTRRK0a0AQ/l04DbmQxy+jVHBVkg6fbzguShdr7ocH2PXE0hwZNDwyO5bCg6H"
    "qO6bBA7oN74mP5aeqzlNZ9U60nW2d7+P5IZu4Aqjc07o2/i16YNvzlM+Q3DuCF0eH5ml07"
    "yCJYVkZko0Z90Xsv+t6L/r9e9EiakD5OiD+t60DmIxvbD1TovPceb6j3uMcJB5caZO8lkw"
    "Pn7t0plrK0YZo7pGmptTZPq7Fyooat0QDiXP1tAtS1Xeqc1Fr/XwhttdIxKjCtKXN/fRle"
    "rylxhUkF5C2VE/wWEF+ctiLCxffjxLqBIsy6VLRyeCdX/X+rXM8+DQfVagQPGEjGBy0vT/"
    "8BA0TXZg=="
)
