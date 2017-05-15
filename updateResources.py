# -*- coding:utf-8 -*-
"""
更新资源通用脚本
"""
import ConfigParser
import os
import sys
from WorkTools import CopyResource
from WorkTools import SvnProcesser as Svn

_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

_resource_config = ConfigParser.ConfigParser()
_resource_config.read(os.path.dirname(os.path.realpath(__file__)) + '/update_resource_config.ini')

_COMMIT_OR_NOT = False


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


def get_src_list(update_kind, shadow_vars):
    src_list = []
    raw_src_path = get_src_path(update_kind)
    if "file_pattern" in _resource_config.options(update_kind) or "file_pattern" in shadow_vars:
        for one_pattern in _resource_config.get(update_kind, "file_pattern", vars=shadow_vars).split('|'):
            src_list.append(raw_src_path + os.path.sep + one_pattern)
    return src_list


def get_sub_kind(kind):
    return _resource_config.get(kind, "update_kind_list").split('|')


def update_src(src_file):
    if not CopyResource.is_from_svn(src_file):
        if os.path.exists(os.path.dirname(src_file)):
            Svn.update(os.path.dirname(src_file))


def start_copy(kind, pattern_input=None):
    if _resource_config.has_section(kind):
        if _resource_config.has_option(kind, "update_kind_list"):
            for sub_kind in get_sub_kind(kind):
                start_copy(sub_kind, pattern_input)
        else:
            vars_dict = {}
            if pattern_input:
                vars_dict["file_pattern"] = pattern_input
            for src_file in get_src_list(kind, vars_dict):
                update_src(src_file)
                CopyResource.copy_file_by_pattern(src_file, get_tar_path(kind))
    else:
        print "no config"
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "need argv"
        print _resource_config.sections()
        exit(1)

    kind = sys.argv[1]

    trunk_path = _config.get("local_file_system", "trunk_path")
    update_src(trunk_path)
    if len(sys.argv) == 2:
        start_copy(kind)
    elif len(sys.argv) == 3:
        name_pattern = sys.argv[2]
        start_copy(kind, name_pattern)

    Svn.status(trunk_path)

    print "commit or not(y/n):",
    commit_or_not = raw_input("commit or not(y/n):")

    if commit_or_not == "y":
        commit_notes = "提交资源"
        if "commit_notes" in _resource_config.options(kind):
            commit_notes = _resource_config.get(kind, "commit_notes")
        Svn.add(trunk_path + "/Resources")
        Svn.commit(trunk_path, commit_notes)
