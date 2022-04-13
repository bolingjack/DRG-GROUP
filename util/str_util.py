# -*- coding:utf8 -*-

"""字符串工具类"""


def is_number(s: "字符串") -> "是否为数字":
    """
    判断字符串是否能转化为数字
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
