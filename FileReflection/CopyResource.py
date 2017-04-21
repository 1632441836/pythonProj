# -*- coding:utf-8 -*-
"""
资源拷贝工具接口
"""
from FileMap import FileMap
import os
import shutil


def copy_file(s_path, t_path):  # TODO
    """从源地址拷贝文件到目标地址"""
    s_path = os.path.normpath(s_path)
    t_path = os.path.normpath(t_path)
    if os.path.exists(s_path):
        if os.path.exists(t_path):
            if os.path.isdir(s_path) and os.path.isdir(t_path):
                pass
        elif os.path.exists(os.path.dirname(t_path)):
            t_path = os.path.dirname(t_path)
            if os.path.isdir(t_path):
                shutil.copy(s_path, t_path)
            else:
                print "copy file error."
                print "target path not right"
                print s_path
                print t_path
        else:
            print "copy file error."
            print "target path doesnt exit"
            print s_path
            print t_path
    else:
        print "copy file error."
        print "source doesnt exist"
        print s_path
        print t_path


def export_file(s_path, t_path):  # TODO
    """从svn中导出文件到目标地址"""
    pass


if __name__ == "__main__":
    f_map = FileMap()
    f_map.read_ini_file()
    source_path = input('input:')
    tar_list = f_map.get_target_list(source_path)
    if tar_list:
        for tar in tar_list:
            copy_file(source_path, tar)
    else:
        target_path = input("信息文件里没有这个路径，请手动输入一次。")
        copy_file(source_path, target_path)
        f_map.add_relation(source_path, target_path)
        f_map.write_back_file()

