# -*- coding:utf8 -*-
"""配置的工具类"""
import configparser
from common.root_path import root_path

config_file_path = root_path + "/config/grouper.cfg"


def get_grouper_version():
    """
    获取分组器版本号
    :return:
    """
    cp = configparser.ConfigParser()
    cp.read(config_file_path)
    grouper_version = cp.get("grouper", "version")
    return grouper_version


def get_grouper_host():
    """
    获取分组服务设置的ip
    :return:
    """
    cp = configparser.ConfigParser()
    cp.read(config_file_path)
    grouper_host = cp.get("grouper", "host")
    return grouper_host


def get_grouper_port():
    """
    获取分组服务设置的端口
    :return:
    """
    cp = configparser.ConfigParser()
    cp.read(config_file_path)
    grouper_port = int(cp.get("grouper", "port"))
    return grouper_port
