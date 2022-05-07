# -*- coding:utf8 -*-
"""模型类"""
from util.config_util import get_grouper_version


class Case(object):
    def __init__(self):
        self.unique_id = ""  # 唯一id
        self.primary_diagnosis_code = ""  # 主要诊断编码
        self.secondary_diagnosis_code_dict = dict([])  # 次要诊断编码字典
        self.major_operation_code = ""  # 主要手术编码
        self.minor_operation_code_dict = dict([])  # 次要手术编码字典
        self.gender = -1  # 性别
        self.age = -1  # 年龄
        self.newborn_age_day = -1  # 新生儿年龄（天）
        self.newborn_birth_weight = -1  # 新生儿出生体重（克）

        self.second_diagnosis_code_list = []  # 次要诊断编码列表
        self.minor_operation_code_list = []  # 次要手术编码列表
        self.have_operation = 0  # 是否有手术

        self.mdc_code = "0000"  # MDC编码
        self.mdc_name = "00组"  # MDC名称
        self.adrg_code = "0000"  # ADRG编码
        self.adrg_name = "00组"  # ADRG名称
        self.drg_code = "0000"  # DRG编码
        self.drg_name = "00组"  # DRG名称
        self.not_into_group_reason = ""  # 未入组原因（仅限00组）
        self.has_mcc = 0  # 是否有严重并发症
        self.has_cc = 0  # 是否有一般并发症
        self.grouper_version = get_grouper_version()  # 分组器版本
