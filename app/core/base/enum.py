from enum import IntEnum


class GenderEnum(IntEnum):
    unkown = 0
    male = 1
    female = 2


GENDER_TEXT_CONVERT = {
    GenderEnum.unkown: '未知',
    GenderEnum.male: '男',
    GenderEnum.female: '女',
}
