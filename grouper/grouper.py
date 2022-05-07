# -*- coding:utf8 -*-

"""工具类"""
from common.grouper_rule_information import grouper_rule_file_path, mdc_information_sheet_name, adrg_information_sheet_name, \
    drg_information_sheet_name, mdc_diagnosis_sheet_name, adrg_diagnosis_sheet_name, adrg_operation_sheet_name, mcc_sheet_name, \
    cc_sheet_name, excluded_diagnosis_sheet_name, drg_group_rule_sheet_name
import pandas as pd
from collections import defaultdict

"""数据读取"""
drg_information_data = pd.read_excel(grouper_rule_file_path, sheet_name=drg_information_sheet_name, dtype=str)
mdc_diagnosis_data = pd.read_excel(grouper_rule_file_path, sheet_name=mdc_diagnosis_sheet_name, dtype=str)
adrg_diagnosis_data = pd.read_excel(grouper_rule_file_path, sheet_name=adrg_diagnosis_sheet_name, dtype=str)
adrg_operation_data = pd.read_excel(grouper_rule_file_path, sheet_name=adrg_operation_sheet_name, dtype=str)
mcc_data = pd.read_excel(grouper_rule_file_path, sheet_name=mcc_sheet_name, dtype=str)
cc_data = pd.read_excel(grouper_rule_file_path, sheet_name=cc_sheet_name, dtype=str)
excluded_diagnosis_data = pd.read_excel(grouper_rule_file_path, sheet_name=excluded_diagnosis_sheet_name, dtype=str)
drg_group_rule_data = pd.read_excel(grouper_rule_file_path, sheet_name=drg_group_rule_sheet_name, dtype=str)
print('分组数据加载完成')
"""数据预处理"""
for data in [drg_information_data, mdc_diagnosis_data, adrg_diagnosis_data, adrg_operation_data, mcc_data, cc_data, excluded_diagnosis_data,
             drg_group_rule_data]:
    for col in data.columns:
        if col in ['op', 'mcc', 'cc']:
            data[col] = data[col].apply(int)
        else:
            data[col] = data[col].apply(lambda x: x.strip())

drg_code_name_dict = drg_information_data.set_index('drg_code').to_dict()['drg_name']


def get_drg_information(case):
    if case.drg_code in drg_code_name_dict:
        case.drg_name = drg_code_name_dict.get(case.drg_code)
    return case


diagnosis_code_mdc_classification_dict = defaultdict(set)  # 诊断编码-mdc分类字典
diagnosis_code_post_mdc_dict = defaultdict(set)  # 诊断编码-后期mdc字典
pre_mdc_list = ['MDCA', 'MDCM', 'MDCN', 'MDCO', 'MDCP', 'MDCY', 'MDCZ']
pre_mdc_set = set(pre_mdc_list)

mdc_diagnosis_data_group_by_diagnosis_code = mdc_diagnosis_data.groupby(['diagnosis_code'])
for value in mdc_diagnosis_data_group_by_diagnosis_code:
    _diagnosis_code, sub_data = value
    diagnosis_code_mdc_classification_dict[_diagnosis_code] = set(sub_data['classification'])
    post_mdc_set = set(sub_data['mdc_code']) - pre_mdc_set
    if post_mdc_set:
        diagnosis_code_post_mdc_dict[_diagnosis_code] = post_mdc_set

diagnosis_code_adrg_classification_dict = defaultdict(set)  # 诊断编码-adrg分类字典
adrg_diagnosis_data_group_by_diagnosis_code = adrg_diagnosis_data.groupby(['diagnosis_code'])
for value in adrg_diagnosis_data_group_by_diagnosis_code:
    _diagnosis_code, sub_data = value
    diagnosis_code_adrg_classification_dict[_diagnosis_code] = set(sub_data['classification'])

operation_code_adrg_classification_dict = defaultdict(set)  # 手术编码-adrg分类字典
adrg_operation_data_group_by_operation_code = adrg_operation_data.groupby(['operation_code'])
for value in adrg_operation_data_group_by_operation_code:
    _operation_code, sub_data = value
    operation_code_adrg_classification_dict[_operation_code] = set(sub_data['classification'])

mcc_excluded_table_dict = mcc_data.set_index('diagnosis_code').to_dict()['excluded_table']
cc_excluded_table_dict = cc_data.set_index('diagnosis_code').to_dict()['excluded_table']
excluded_table_list_dict = defaultdict(set)  # 各类排除诊断列表
excluded_diagnosis_data_group_by_table_name = excluded_diagnosis_data.groupby(['table_name'])
for value in excluded_diagnosis_data_group_by_table_name:
    _table_name, sub_data = value
    excluded_table_list_dict[_table_name] = set(sub_data['diagnosis_code'])


def is_pd1(case, mdc_classification):  # 判断主要诊断是否在MDC诊断表中
    flag = 0
    if case.primary_diagnosis_code in diagnosis_code_mdc_classification_dict and mdc_classification in \
            diagnosis_code_mdc_classification_dict[case.primary_diagnosis_code]:
        flag = 1
    return flag


def is_pd2(case, adrg_classification):  # 判断主要诊断是否在ADRG诊断表中
    flag = 0
    if case.primary_diagnosis_code in diagnosis_code_adrg_classification_dict and adrg_classification in \
            diagnosis_code_adrg_classification_dict[case.primary_diagnosis_code]:
        flag = 1
    return flag


def is_sd1(case, mdc_classification):  # 判断次要诊断是否在MDC诊断表中
    flag = 0
    for second_diagnosis_code in case.second_diagnosis_code_list:
        if second_diagnosis_code in diagnosis_code_mdc_classification_dict and mdc_classification in diagnosis_code_mdc_classification_dict[
            second_diagnosis_code]:
            flag = 1
            break
    return flag


def is_sd2(case, adrg_classification):  # 判断次要诊断是否在ADRG诊断表中
    flag = 0
    for second_diagnosis_code in case.second_diagnosis_code_list:
        if second_diagnosis_code in diagnosis_code_adrg_classification_dict and adrg_classification in \
                diagnosis_code_adrg_classification_dict[second_diagnosis_code]:
            flag = 1
            break
    return flag


def is_op2(case, adrg_classification):  # 判断手术是否在ADRG手术表中
    flag = 0
    for operation in case.operation_code_list:
        if operation in operation_code_adrg_classification_dict and adrg_classification in operation_code_adrg_classification_dict[
            operation]:
            flag = 1
            break
    return flag


def multi_wound(case):  # 判断是否为多发创伤
    flag = 0
    if case.primary_diagnosis_code and case.second_diagnosis_code_list:
        classification_set = set([])
        if case.primary_diagnosis_code in diagnosis_code_mdc_classification_dict:
            for classification in diagnosis_code_mdc_classification_dict[case.primary_diagnosis_code]:
                if classification.startswith("Z"):
                    classification_set.add(classification)
            if len(classification_set) > 0:  # 主诊必须是MDCZ
                for diagnosis_code in case.second_diagnosis_code_list:
                    if diagnosis_code in diagnosis_code_mdc_classification_dict:
                        for classification in diagnosis_code_mdc_classification_dict[diagnosis_code]:
                            if classification.startswith("Z"):
                                classification_set.add(classification)
                if len(classification_set) >= 2:
                    flag = 1
    return flag


def is_mcc(case):  # 是否有严重并发症与合并症
    flag = 0
    if case.primary_diagnosis_code and case.second_diagnosis_code_list:
        for second_diagnosis_code in case.second_diagnosis_code_list:
            if second_diagnosis_code in mcc_excluded_table_dict and case.primary_diagnosis_code not in excluded_table_list_dict[
                mcc_excluded_table_dict[second_diagnosis_code]]:
                flag = 1
    return flag


def is_cc(case):  # 是否有一般并发症与合并症
    flag = 0
    if case.primary_diagnosis_code and case.second_diagnosis_code_list:
        for second_diagnosis_code in case.second_diagnosis_code_list:
            if second_diagnosis_code in cc_excluded_table_dict and case.primary_diagnosis_code not in excluded_table_list_dict[
                cc_excluded_table_dict[second_diagnosis_code]]:
                flag = 1
    return flag


def diagnosis_transform(diagnosis_code):  # 诊断转换
    if diagnosis_code and "." in diagnosis_code and diagnosis_code.index('.') == 3:
        return diagnosis_code.strip()
    return ''


def operation_transform(operation_code):  # 手术转换
    if operation_code and '.' in operation_code and operation_code.index('.') == 2:
        return operation_code.strip()
    return ''


drg_group_rule_data_a1 = drg_group_rule_data[
    (drg_group_rule_data['mdc_code'] == 'MDCA') & (drg_group_rule_data['adrg_code'] != 'MDC')].reset_index(
    drop=True)  # DRG先期分组1（MDCA下属各ADRG）
drg_group_rule_data_a2 = drg_group_rule_data[
    (drg_group_rule_data['mdc_code'] == 'MDCA') & (drg_group_rule_data['adrg_code'] == 'MDC')].reset_index(
    drop=True)  # DRG先期分组2（MDCP、MDCY、MDCZ、MDCM、MDCN、MDCO）
drg_group_rule_data_pre = drg_group_rule_data[
    (drg_group_rule_data['mdc_code'] != 'MDCA') & (drg_group_rule_data['mdc_code'].isin(pre_mdc_list))]  # DRG先期分组
drg_group_rule_data_post = drg_group_rule_data[
    (drg_group_rule_data['mdc_code'] != 'MDCA') & (drg_group_rule_data['mdc_rule'].notnull())]  # 后期分组


def pre_drg_group(case):  # 先期分组
    drg_group_rule_data_a1_drg = drg_group_rule_data_a1[
        (drg_group_rule_data_a1['op'] == case.have_operation) & (drg_group_rule_data_a1['mcc'].isin([-1, case.mcc])) & (
            drg_group_rule_data_a1['cc'].isin([-1, case.cc]))]  # 满足除分组规则之外的其他分组条件
    if len(drg_group_rule_data_a1_drg) != 0:
        drg_group_rule_data_a1_drg.reset_index(drop=True, inplace=True)
        for i in range(len(drg_group_rule_data_a1_drg)):
            _mdc_code, _adrg_code, _drg_code, _, adrg_rule, _, _, _, _ = drg_group_rule_data_a1_drg.loc[i]
            if eval(adrg_rule):
                case.mdc_code = _mdc_code
                case.adrg_code = _adrg_code
                case.drg_code = _drg_code
                break
    if case.mdc_code == '0000':
        for i in range(len(drg_group_rule_data_a2)):
            _mdc_code, _adrg_code, _drg_code, mdc_rule, _, _, _, _, _ = drg_group_rule_data_a2.loc[i]
            if eval(mdc_rule):
                case.mdc_code = _drg_code
                break
    return case


def drg_group(case):  # 分组主程序
    case = pre_drg_group(case)
    if case.mdc_code != 'MDCA':  # A组，结束分组
        mdc_code_list = []
        drg_group_rule_data_mdc = None
        if case.mdc_code != '0000':  # 非A组外的其他先期分组
            mdc_code_list.append(case.mdc_code)
            drg_group_rule_data_mdc = drg_group_rule_data_pre[drg_group_rule_data_pre['mdc_code'].isin(mdc_code_list)]
        else:  # 后期分组
            if case.primary_diagnosis_code and case.primary_diagnosis_code in diagnosis_code_post_mdc_dict:  # 主要诊断不在诊断编码-mdc2字典中
                mdc_code_list.extend(list(diagnosis_code_post_mdc_dict[case.primary_diagnosis_code]))
                drg_group_rule_data_mdc = drg_group_rule_data_post[drg_group_rule_data_post['mdc_code'].isin(mdc_code_list)]
        if mdc_code_list:
            drg_group_rule_data_drg = drg_group_rule_data_mdc[
                (drg_group_rule_data_mdc['op'].isin([case.have_operation])) & (drg_group_rule_data_mdc['mcc'].isin([-1, case.mcc])) & (
                    drg_group_rule_data_mdc['cc'].isin([-1, case.cc]))]  # 满足除分组规则之外的其他分组条件
            case.mdc_code = mdc_code_list[0]
            if len(drg_group_rule_data_drg) > 0:
                drg_group_rule_data_drg.reset_index(drop=True, inplace=True)
                for i in range(len(drg_group_rule_data_drg)):
                    _mdc_code, _adrg_code, _drg_code, _, adrg_rule, drg_rule, _, _, _ = drg_group_rule_data_drg.loc[i]
                    adrg_flag = eval(adrg_rule)
                    drg_flag = eval(drg_rule)
                    if adrg_flag:  # 满足adrg标记
                        case.mdc_code = _mdc_code
                        case.adrg_code = _adrg_code
                        if drg_flag:  # 满足drg标记
                            case.drg_code = _drg_code
                            break
    case = get_drg_information(case)
    return case


def drg_grouper(case):
    try:
        # 处理主要诊断编码
        tmp_diagnosis_code = diagnosis_transform(case.primary_diagnosis_code)
        if tmp_diagnosis_code:
            case.primary_diagnosis_code = tmp_diagnosis_code

        # 处理其他诊断编码
        for key in case.second_diagnosis_codes:
            tmp_diagnosis_code = diagnosis_transform(case.second_diagnosis_codes[key])
            if tmp_diagnosis_code:
                case.second_diagnosis_code_list.append(tmp_diagnosis_code)

        # 处理手术及操作编码
        for key in case.operation_codes:
            tmp_operation_code = operation_transform(case.operation_codes[key])
            if tmp_operation_code and tmp_operation_code in operation_code_adrg_classification_dict:
                case.operation_code_list.append(tmp_operation_code)

        if case.operation_code_list:
            case.have_operation = 1
        # 处理伴随症及合并症
        case.has_mcc = is_mcc(case)
        case.has_cc = is_cc(case)
        case.mcc = case.has_mcc
        if case.mcc:
            case.cc = 0
        else:
            case.cc = case.has_cc
        try:
            case = drg_group(case)
        except:
            case.mdc_code = case.adrg_code = case.drg_code = 'error_inner'
    except:
        case.mdc_code = case.adrg_code = case.drg_code = 'error_outer'
    return case
