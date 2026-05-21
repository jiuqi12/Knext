from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `userroles` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(30) NOT NULL UNIQUE COMMENT '角色名',
    `service_accounts` VARCHAR(30) NOT NULL COMMENT '服务账号',
    `namespace` VARCHAR(30) NOT NULL COMMENT '命名空间',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(30) NOT NULL UNIQUE COMMENT '用户名',
    `hash_password` VARCHAR(118) NOT NULL COMMENT '密码',
    `is_active` BOOL NOT NULL COMMENT '是否启用改账号' DEFAULT 1,
    `login_attempts` INT NOT NULL COMMENT '登录错误次数，超过三次禁用账号' DEFAULT 0,
    `is_admin` BOOL NOT NULL COMMENT '是否是管理员' DEFAULT 0,
    `email` VARCHAR(30) NOT NULL COMMENT '邮箱',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `last_login_attempt` DATETIME(6) COMMENT '最后登录尝试时间',
    `role_id` INT NOT NULL COMMENT '角色ID',
    CONSTRAINT `fk_user_userrole_c8bc91ea` FOREIGN KEY (`role_id`) REFERENCES `userroles` (`id`) ON DELETE CASCADE
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
    "eJztmW1v4jgQgP8K4lNP2lslgbxw34BSLbfbcmrp3WmXVeQkDlhNHDZx2kUr/vuNHfJKoK"
    "RHWyr1C4XxTGI/M54Zu7/afuBgL/p4G+Gw/UfrV5siH8OXkvxDq42Wy1zKBQxZnlCMUw0r"
    "YiGyGchc5EUYRA6O7JAsGQkoSGnseVwY2KBI6DwXxZT8iLHJgjlmCzGPb99BTKiDf+Io/b"
    "m8M12CPac0TeLwdwu5yVZLIRtTdiEU+dss0w682Ke58nLFFgHNtAllXDrHFIeIYf54FsZ8"
    "+nx2m1WmK0pmmqskUyzYONhFsccKyz2QgR1Qzg9mE4kFzvlbflfkrt41OlrXABUxk0yir5"
    "Pl5WtPDAWBq2l7LcYRQ4mGwJhz414T37foDRcorMdXtKlAhKlXIabInoFiexbrqmLMYk3p"
    "6LNY7UrJZB+n6qOfpofpnC3gZ0fag/Dv/vXwU//6rCP9xp8dQGgn8X61GVHEEKecU12gaG"
    "EuURQ9BGFNYO5Gu2V4HL6pIAecb83HCKuWrQFnQ5KfwlaWjQPggtZOumKsjJdEJiQYcl8T"
    "tYMg8DCiO/Z90a5C1gLD50KbRXMFraYpLg9bRROfbhbOaqc3iw1HyDuufhj4PZwHk8kX/h"
    "A/in54QjCeVnjfXg5G4AjhBlAiDBcTSM7eC+aEmogx7C9Z1CDpbhs+noCP5QCpNnVougV8"
    "XVWdxT1V5sQtDD7QLEXmPtClWey6ks09YYCO4dqQZLpY6qU6es+QU5819dZxEnt5Tzg+oU"
    "/YEqnZC+6I+s6gsiWS77qFOOSuJDaJapzSZsA+Il6T/J4ZvH5e70kIc7rWk/L68WumHWK+"
    "csgQ20DPYYQRH9dDLVtWyDob04/plxevn4rM0wzo8aTiajzZuN0DmcPKnAn1Vpsisof5dH"
    "w5upn2L/8qhfZ5fzriI4qQrirSM63in+whrX/G008t/rP1dXI1ElyDiM1D8cZcb/q1zeeE"
    "YhaYNHiAXFLo3lJpiqtcR1DEzFJNaOr2+iccwf2b6R/F+5ouSaIzxeWCo9qywwuOozaPij"
    "cSBSmkvWEQQm0yGx3eChYv10Dscq/RcxT4VHRlfP5ydZ+fgt272vMcp7MN8yIIMZnTz3gl"
    "mI5hRojadW1w4bh/DY+KTh/oOg2QVJrv4BA9ZFcFxbiB9cIqcVLVh/2bYf981BZULWTfPa"
    "DQMUt4+UigBBVJprs95Ct+VYIomgsWfBV8zlukd9y6ZG7Yf/USZmrv9y+PR9rJ3L80vXs5"
    "lXuXfJ+e0r0L7IN7YmM45dtBTOuOp7vJ1tm+fpcO/YPDe0h+Bmp8xHxm2vxvtER24wDOjF"
    "6fr9rVnSSCoT9DOmrUnb+fiN5PRP/vRLTVye1uQsp39jWpbbAxu/h8jT0kcO/t795ua7d+"
    "zoasj0NiL+q6sc3I3lYM5Trvfdgb6sPuYUttdsyhlaxg8sp17HCKpYqlqOoBJQu0dtYsMV"
    "YuWnxrNIC4UX+bAGXpkJoPWrv/uSVtV/2AMkxrSv6fN5OrHeU+N6mAvKWwwG8OsdmHlkci"
    "9v00se6hyFddKuApvLPL/r9VrsMvk0G1MvMHDOouTV7yvL/+Dxl5neg="
)
