from enum import IntEnum


class GenderEnum(IntEnum):
    UNKOWN = 0
    MALE = 1
    FEMALE = 2


GENDER_TEXT_CONVERT = {
    GenderEnum.UNKOWN: '未知',
    GenderEnum.MALE: '男',
    GenderEnum.FEMALE: '女',
}
