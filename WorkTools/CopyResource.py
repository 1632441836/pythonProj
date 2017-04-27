# -*- coding:utf-8 -*-
"""
资源拷贝工具接口
"""
from FileReflection.FileMap import FileMap
import os
import shutil
import ConfigParser
import glob
import commands
from WorkTools import SvnProcesser as Svn
from WorkTools import RedmineProcesser as Redmine


_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/../config.ini')


def copy_file(s_path, t_path):
    """
    从源路径向目标路径拷贝文件
    :param s_path: 源路径
    :param t_path: 目标路径
    :return:
    """
    s_path = os.path.normpath(s_path)
    t_path = os.path.normpath(t_path)
    shell_command = "cp -r %s %s"
    print s_path
    print t_path
    if os.path.exists(s_path):
        if os.path.isdir(s_path):
            if os.path.isdir(t_path):
                if os.path.basename(s_path) == os.path.basename(t_path):
                    print commands.getoutput(shell_command % (s_path, os.path.dirname(t_path)))
                else:
                    print commands.getoutput(shell_command % (s_path, t_path))
            else:
                raise Exception("plz check the paths, source is dir but target is file.", s_path, t_path)
        else:
            if os.path.exists(t_path):
                if os.path.isdir(t_path):
                    print commands.getoutput(shell_command % (s_path, t_path))
                else:
                    print commands.getoutput(shell_command % (s_path, t_path))
            else:
                if os.path.isdir(os.path.dirname(t_path)):
                    print commands.getoutput(shell_command % (s_path, t_path))
                else:
                    raise Exception("plz check the paths, dir of target file doesnt exist.", s_path, t_path)
    else:
        raise Exception("source path doesnt exist.", s_path, t_path)


def copy_file_by_pattern(s_path, t_path):
    """
    复制文件，使用了glob模块因此可以使用通配符
    :param s_path:源文件
    :param t_path:目标文件
    :return:
    """
    file_list = glob.glob(s_path)
    for one_file in file_list:
        copy_file(one_file, t_path)


def export_file(s_path, t_path):
    """
    从svn导出文件到目标地址
    :param s_path: svn的地址
    :param t_path: 目标地址
    :return:
    """
    if os.path.exists(t_path):
        # 目标地址存在直接导出
        if os.path.basename(s_path) == os.path.basename(t_path):
            # 名字一致
            Svn.export_file_forced(s_path, t_path)
        else:
            # 名字不一致给续个名字
            Svn.export_file_forced(s_path, t_path + os.path.sep + os.path.basename(s_path))
    else:
        # 目标地址不存在，查看目标地址父级目录是否存在，若存在且目标目录名字和源目录名字一致，那么也导出出去。
        if os.path.exists(os.path.dirname(t_path)) and os.path.basename(s_path) == os.path.basename(t_path):
            Svn.export_file_forced(s_path, os.path.dirname(t_path))
        else:
            print "export error"
            return -1


def is_from_svn(path):
    """
    判断地址中是否含有svn的地址
    :param path: 地址
    :return:
    """
    svn_root = _config.get("remote_url", "svn_root")
    if path.find(svn_root) != -1:
        return True
    else:
        return False


def translate_files(s_path, t_path):
    """
    从源路径向目标路径转移文件
    :param s_path: 源路径
    :param t_path: 目标路径
    :return:
    """
    if is_from_svn(s_path):
        export_file(s_path, t_path)
    else:
        copy_file(s_path, t_path)


if __name__ == "__main__":
    f_map = FileMap()
    f_map.read_ini_file()
    source_path = input('input:')
    tar_list = f_map.get_target_list(source_path)
    if tar_list:
        for tar in tar_list:
            translate_files(source_path, tar)
    else:
        target_path = input("信息文件里没有这个路径，请手动输入一次。")
        copy_file(source_path, target_path)
        f_map.add_relation(source_path, target_path)
        f_map.write_back_file()

