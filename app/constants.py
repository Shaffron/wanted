from enum import EnumMeta


class LANGUAGE(EnumMeta):
    KOREAN = 'ko'
    ENGLISH = 'en'
    JAPANESE = 'jp'


class WORD(EnumMeta):
    KOREAN = '태그'
    ENGLISH = 'tag'
    JAPANESE = 'タグ'
