from enum import Enum


class AccountErrorEnum(Enum):
    ALL_OK = -1
    NOT_EXISTS = 0
    EXISTED = 1
    INVALID_OTP = 2
    INCORRECT_PASSWORD = 3
    WEAK_PASSWORD = 4