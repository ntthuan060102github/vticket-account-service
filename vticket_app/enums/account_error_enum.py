from enum import Enum


class AccountErrorEnum(Enum):
    ALL_OK = -1
    NOT_EXISTS = 0
    EXISTED = 1
    INVALID_OTP = 2