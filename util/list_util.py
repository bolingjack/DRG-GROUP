# -*- coding:utf8 -*-
"""涉及列表操作的工具类"""


def duplicates(duplicated_list: "去重的列表", keep_order: "是否保持有序" = False) -> "去重后的列表":
    """
    对列表去重
    :param duplicated_list:需要去重的列表
    :param keep_order:是否保持原有顺序
    :return:
    """
    if keep_order:
        list2 = []
        for i in duplicated_list:
            if i not in list2:
                list2.append(i)
        return list2
    else:
        return list(set(duplicated_list))



