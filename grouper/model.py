# -*- coding:utf8 -*-
"""模型类"""
from util.config_util import get_grouper_version


class Case(object):
    def __init__(self):
        self.unique_id = ""  # 唯一id
        self.primary_diagnosis_code = ""  # 主要诊断编码
        self.second_diagnosis_codes = dict([])  # 次要诊断编码字典
        self.operation_codes = dict([])  # 手术编码字典
        self.gender = -1  # 性别
        self.age = -1  # 年龄
        self.in_hospital_day = -1  # 实际住院天数
        self.newborn_age_month = -1  # 新生儿年龄（月）
        self.newborn_birth_weight = -1  # 新生儿出生体重（克）
        self.in_hospital_cost = -1  # 住院总费用

        self.second_diagnosis_code_list = []  # 次要诊断编码列表
        self.major_operation_code = ""
        self.operation_code_list = []  # 手术编码列表
        self.have_operation = 0  # 是否有手术

        self.excluded_flag = 0
        self.excluded_reason = ""
        self.mdc_code = "0000"
        self.adrg_code = "0000"
        self.drg_code = "0000"
        self.drg_name = "00组"
        self.exception_type = ""  #
        self.has_mcc = 0
        self.has_cc = 0
        self.grouper_version = get_grouper_version()  # 分组器版本
