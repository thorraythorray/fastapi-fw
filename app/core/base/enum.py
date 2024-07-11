from enum import Enum, IntEnum


# class GenderEnum(IntEnum):
#     unkown = 0
#     male = 1
#     female = 2


class GenderEnum(str, Enum):
    unkown = '不明'
    male = '男性'
    female = '女性'
