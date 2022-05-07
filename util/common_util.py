# -*- coding:utf8 -*-

"""普通工具类"""
from grouper.grouper import diagnosis_code_mdc_classification_dict
from util.str_util import is_number

gender_list = [0, 1, 2, 9]
standard_secondary_diagnosis_key_list = ["secondary_diagnosis_code" + str(i) for i in range(1, 51)]
standard_minor_operation_key_list = ["operation_code" + str(i) for i in range(1, 21)]


def check_and_transform_field(case, input_dict):
    """
    对传入的参数进行校验，并返回转换后的字段字典
    :param case:
    :param input_dict:
    :return:
    """
    if "unique_id" in input_dict and len(input_dict['unique_id']) > 0:
        case.unique_id = input_dict['unique_id'].strip()
    if "primary_diagnosis_code" in input_dict and len(input_dict['primary_diagnosis_code']) > 0:
        case.primary_diagnosis_code = input_dict['primary_diagnosis_code'].strip()
    if "secondary_diagnosis_code_dict" in input_dict and type(input_dict['secondary_diagnosis_code_dict']) is dict:
        for key in input_dict['secondary_diagnosis_code_dict']:
            if key in standard_secondary_diagnosis_key_list and len(input_dict['secondary_diagnosis_code_dict'][key].strip()) > 0:
                case.second_diagnosis_codes[key] = input_dict['secondary_diagnosis_code_dict'][key].strip()
    if "major_operation_code" in input_dict and len(input_dict['major_operation_code']) > 0:
        case.major_operation_code = input_dict['major_operation_code'].strip()
    if "minor_operation_code_dict" in input_dict and type(input_dict['minor_operation_code_dict']) is dict:
        for key in input_dict['minor_operation_code_dict']:
            if key in standard_minor_operation_key_list and len(input_dict['minor_operation_code_dict'][key].strip()) > 0:
                case.operation_codes[key] = input_dict['minor_operation_code_dict'][key].strip()
    if "gender" in input_dict and input_dict['gender'] in gender_list:
        case.gender = input_dict['gender']
    if "age" in input_dict and is_number(input_dict['age']) and input_dict['age'] >= 0:
        case.age = input_dict['age']
    if "newborn_age_month" in input_dict and is_number(input_dict['newborn_age_month']) and input_dict['newborn_age_month'] >= 0:
        case.newborn_age_month = input_dict['newborn_age_month']
    if "newborn_birth_weight" in input_dict and is_number(input_dict['newborn_birth_weight']) and input_dict['newborn_birth_weight'] >= 0:
        case.newborn_birth_weight = input_dict['newborn_birth_weight']
    return case


def get_not_into_group_reason(case):
    """
    未入组原因
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
