# -*- coding:utf8 -*-

"""普通工具类"""
from grouper.grouper import diagnosis_code_mdc_classification_dict
from util.str_util import is_number

gender_list = [0, 1, 2, 9]
standard_second_diagnosis_code_list = ["second_diagnosis_code" + str(i) for i in range(1, 51)]
standard_operation_code_list = ["operation_code" + str(i) for i in range(1, 21)]


def check_and_transform_field(case, input_dict):
    """
    对传入的参数进行校验，并返回转换后的字段字典
    :param input_dict:
    :return:
    """
    if "unique_id" in input_dict and len(input_dict['unique_id']) > 0:
        case.unique_id = input_dict['unique_id'].strip()
    if "primary_diagnosis_code" in input_dict and len(input_dict['primary_diagnosis_code']) > 0:
        case.primary_diagnosis_code = input_dict['primary_diagnosis_code'].strip()
    if "second_diagnosis_codes" in input_dict and type(input_dict['second_diagnosis_codes']) is dict:
        for key in input_dict['second_diagnosis_codes']:
            if key in standard_second_diagnosis_code_list and len(input_dict['second_diagnosis_codes'][key].strip()) > 0:
                case.second_diagnosis_codes[key] = input_dict['second_diagnosis_codes'][key].strip()
    if "operation_codes" in input_dict and type(input_dict['operation_codes']) is dict:
        for key in input_dict['operation_codes']:
            if key in standard_operation_code_list and len(input_dict['operation_codes'][key].strip()) > 0:
                case.operation_codes[key] = input_dict['operation_codes'][key].strip()
    if "gender" in input_dict and input_dict['gender'] in gender_list:
        case.gender = input_dict['gender']
    if "age" in input_dict and is_number(input_dict['age']) and input_dict['age'] >= 0:
        case.age = input_dict['age']
    if "in_hospital_day" in input_dict and is_number(input_dict['in_hospital_day']) and input_dict['in_hospital_day'] >= 0:
        case.in_hospital_day = input_dict['in_hospital_day']
    if "newborn_age_month" in input_dict and is_number(input_dict['newborn_age_month']) and input_dict['newborn_age_month'] >= 0:
        case.newborn_age_month = input_dict['newborn_age_month']
    if "newborn_birth_weight" in input_dict and is_number(input_dict['newborn_birth_weight']) and input_dict['newborn_birth_weight'] >= 0:
        case.newborn_birth_weight = input_dict['newborn_birth_weight']
    if "in_hospital_cost" in input_dict and is_number(input_dict['in_hospital_cost']) and input_dict['in_hospital_cost'] >= 0:
        case.in_hospital_cost = input_dict['in_hospital_cost']
    return case


def check_excluded(case):
    """
    查看病例是否为排除病例，并返回原因
    :param case:
    :return:
    """
    if case.in_hospital_day == -1:
        case.excluded_flag = 1
        case.excluded_reason = "实际住院天数缺失或错误"
    elif case.in_hospital_day > 60:
        case.excluded_flag = 1
        case.excluded_reason = "实际住院天数大于60天"
    elif case.in_hospital_cost == -1:
        case.excluded_flag = 1
        case.excluded_reason = '总费用缺失或错误'
    elif case.in_hospital_cost < 5:
        case.excluded_flag = 1
        case.excluded_reason = '总费用小于5元'
    elif case.primary_diagnosis_code.startswith("Z53") and case.in_hospital_day <= 2:
        case.excluded_flag = 1
        case.excluded_reason = "主要诊断代码以Z53开头且实际住院天数小于等于2天"
    return case


def get_exception_type(case):
    """
    查看DRG分组结果为0000组的原因
    :param mdc:MDC编码
    :param adrg:ADRG编码
    :param drg:DRG编码
    :param case:病例对象
    :return:
    """
    case.exception_type = '未定义的错误'
    if case.mdc_code == '0000':
        if case.primary_diagnosis_code == "":
            case.exception_type = "主要诊断缺失"
        elif diagnosis_code_mdc_classification_dict[case.primary_diagnosis_code] & {"P00"}:
            case.exception_type = '主要诊断与年龄冲突'
        elif diagnosis_code_mdc_classification_dict[case.primary_diagnosis_code] & {"M00", "N00", "O00"}:
            case.exception_type = '主要诊断与性别冲突'
        else:
            case.exception_type = "主要诊断不符合分组标准"
    elif case.adrg_code == '0000':
        if case.mdc_code == 'MDCP':
            case.exception_type = '主要诊断与出生体重冲突'
    return case
