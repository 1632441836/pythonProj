# -*- coding:utf-8 -*-
"""
更新资源通用脚本
"""
import sys
from FileReflection import CopyResource
import ConfigParser
import os


_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

_resource_config = ConfigParser.ConfigParser()
_resource_config.read(os.path.dirname(os.path.realpath(__file__)) + '/update_resource_config.ini')


def get_src_path(update_kind):
    result_path = ""
    option_list = _resource_config.options(update_kind)
    if "src_path_section" in option_list and "src_path_option" in option_list:
        path_section = _resource_config.get(update_kind, "src_path_section")
        path_option = _resource_config.get(update_kind, "src_path_option")
        result_path += _config.get(path_section, path_option)
    if "src_path_tail" in option_list:
        result_path += _resource_config.get(update_kind, "src_path_tail")
    return result_path


def get_tar_path(update_kind):
    result_path = ""
    option_list = _resource_config.options(update_kind)
    if "tar_path_section" in option_list and "tar_path_option" in option_list:
        path_section = _resource_config.get(update_kind, "tar_path_section")
        path_option = _resource_config.get(update_kind, "tar_path_option")
        result_path += _config.get(path_section, path_option)
    if "tar_path_tail" in option_list:
        result_path += _resource_config.get(update_kind, "tar_path_tail")
    return result_path


def get_src_list(update_kind):
    src_list = []
    raw_src_path = get_src_path(update_kind)
    if "file_pattern" in _resource_config.options(update_kind):
        for one_pattern in _resource_config.get(update_kind, "file_pattern").split('|'):
            src_list.append(raw_src_path + os.path.sep + one_pattern)
    return src_list


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print "need argv"
    #     exit(1)

    # # 更新战斗中赏金猎人相关的文字图片
    # source_path = _config.get("local_file_system", "art_ani_path") + "/特效/功能特效/赏金猎人/战斗数字"
    # output_path = _config.get("local_file_system", "trunk_path") + "/Resources/images/battle/number"
    #
    # CopyResource.copy_file_by_pattern(source_path + "/*.png", output_path)
    # CopyResource.copy_file_by_pattern(source_path + "/*.plist", output_path)

    kind = "battle_hunter"
    if _resource_config.has_section(kind):
        for src_file in get_src_list(kind):
            CopyResource.copy_file_by_pattern(src_file, get_tar_path(kind))
    else:
        print "no config"
        exit(1)

