from enum import Enum


class codeEnum(Enum):
    """
    返回码类型枚举
    """
    # 业务成功统一状态码
    SUCCESS_CODE = 0
    # 业务已存在
    EXIT_CODE = 10000
    # 业务不存在
    NOT_EXIT_CODE = 10001
    # 系统错误
    SYSTEM_ERROR = 99999
    # 数据非法
    KEY_MISS = 99998
    # 请求数据过长
    DATA_TO_LONG = 99997
    # 数据不能为空
    DATA_NOT_NULL = 10003


VERIFY_NOT_BASE64 = {
    "code": codeEnum.KEY_MISS.value,
    "massage": "系统错误"
}

VERIFY_SUCC = {
    "code": codeEnum.SUCCESS_CODE.value,
    "massage": ""
}
