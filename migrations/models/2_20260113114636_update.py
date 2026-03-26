from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `department` VARCHAR(13) NOT NULL COMMENT '属于部门';
        ALTER TABLE `user` ADD `email` VARCHAR(22) NOT NULL COMMENT '邮箱';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP COLUMN `department`;
        ALTER TABLE `user` DROP COLUMN `email`;"""


MODELS_STATE = (
    "eJztlm1PnEAQx7+KuVc2sQ0Pt4B9d5o0bdNqYmvTxDNkgYHbCAuyiw8xfvfuLHcHnKBobK"
    "4mfUPgPzPLzI/ZYe8mWR5BKj6cCignH3fuJpxmoG46+t7OhBZFo6IgaZBqx2rlEQhZ0lAq"
    "LaapACVFIMKSFZLlXKm8SlMU81A5Mp40UsXZZQW+zBOQC53H2bmSGY/gBsTqsbjwYwZp1E"
    "mTRfhurfvyttDaFy4/aUd8W+CHeVplvHEubuUi52tvxiWqCXAoqQRcXpYVpo/ZLatcVVRn"
    "2rjUKbZiIohplcpWuSMZhDlHfioboQtM8C3vLXPqTj3bmXrKRWeyVtz7urym9jpQEzj6Ob"
    "nXdipp7aExNtzwq+n7B/QOF7Tsx9eO2YCoUt+EuEL2FyhO5pVLLG9eOZbtzisyNepkn6aa"
    "0Rs/BZ7IhXo0zUcQ/pqdHH6eneya5jtcO1etXff70dJiaRNSbqgWVIjrvOzpyWGq7ZjXob"
    "oSGqzNhnyKKwlCR9H1DPNFRJ0xRJ1hos4mUSZ8NVPYVU+jDm/zdszTu/21kNp9PL3IUjyJ"
    "Has+dR03UPcxIapzA8tUV+Ia8yqOjVDplhmp636IPrapoqZgU3ttjomNhsirDQZGx9rLwD"
    "gb4npXjPxurzJfmu8EGWXpc9p+HbD9nt83KCh2QfCinresET1vWYM9j6YuywgKWsoM6lYd"
    "C7QbtX2qJCSA3ekBEgbVtvsExnZnd6rYY6aKPTxVbCSMR4j4ovUzRCGg4cU1LSP/gSW38i"
    "Hfh6bMyjYVymmiiWGFmP/yQDWDkoWLvqPW0vLoYYs2Pv+PW2/ouHUFpcCUnrGfWyFb3szj"
    "KXYHIyFjJiMhw6MRbd3ZiFvjGRCX7m8ToGkYYwafYQxPPrR1Aao3yt4/y9cfx0f9EFshGy"
    "BPuSrwLGKh3NtJmZDn/ybWRyhi1Zh0JsRl2oa3+332e5Pr4bfjA00hFzIp9Sp6gYNt/17u"
    "/wB/bQCb"
)
