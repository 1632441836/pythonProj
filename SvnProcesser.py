# -*- coding:utf-8 -*-
"""
使用svn相关的函数
"""

import commands
import subprocess
import ConfigParser
import re
import os


_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')


def commit(file_path, note):
    shell_command = "svn " + "commit " + "-m '" + note + "' " + file_path
    print shell_command
    out_put = subprocess.check_output(shell_command, shell=True, env={'LANG': 'zh_CN.UTF-8'})
    print out_put
    match = re.search(r'(?<=Committed revision )\d{6}(?=\.)', out_put)
    if match:
        return match.group()


def update(file_path):
    shell_command = "svn update " + file_path
    print commands.getoutput(shell_command)


def revert(file_path):
    shell_command = "svn revert -R " + file_path
    print commands.getoutput(shell_command)


def add(file_path):
    if os.path.isdir(file_path):
        shell_command = "svn st " + file_path
        status_log = commands.getoutput(shell_command)
        string_pattern = r"(\S)(\s*)(\S*)(?=\n)"
        matchs = re.finditer(string_pattern, status_log)
        if matchs:
            for match in matchs:
                if match.group(1) == '?':
                    shell_command = "svn add " + match.group(3)
                    print commands.getoutput(shell_command)
                else:
                    print match.group(0)
    elif os.path.isfile(file_path):
        shell_command = "svn add " + file_path
        print commands.getoutput(shell_command)


def delete(file_path):
    shell_command = "svn rm " + file_path
    print commands.getoutput(shell_command)


def copy_file(sour_path, des_path):
    shell_command = ""
    if os.path.isfile(sour_path):
        shell_command = "cp " + sour_path + ' ' + des_path
    elif os.path.isdir(sour_path):
        shell_command = "cp -r " + sour_path + ' ' + des_path
    if shell_command:
        print commands.getoutput(shell_command)


def get_modified_files(revision):
    shell_command = 'svn log -v -r ' + str(revision) + ' ' + _config.get('local_file_system', 'trunk_path')
    svn_log = commands.getoutput(shell_command)
    file_dictionary = {}
    remote_root = _config.get("remote_url", "remote_file_root")
    string_pattern = r'((?<=  )\w)( )(\S*)((?<=' + remote_root + r'/)\S*(?=\n| ))'
    p = re.finditer(string_pattern, svn_log)
    for i in p:
        file_dictionary[i.group(4)] = i.group(1)
    return file_dictionary


def copy_file_to_online(revision):
    file_dict = get_modified_files(revision)
    trunk_path = _config.get('local_file_system', 'trunk_path')
    online_path = _config.get('local_file_system', 'online_path')
    print file_dict
    for file_name in file_dict:
        if file_dict[file_name] == 'M':
            copy_file(trunk_path + '/' + file_name, online_path + '/' + file_name)
        elif file_dict[file_name] == 'A':
            copy_file(trunk_path + '/' + file_name, online_path + '/' + file_name)
            add(online_path + file_name)
        elif file_dict[file_name] == 'D':
            delete(online_path + '/' + file_name)
        else:
            print "No such status."
            print file_name + ' ' + file_dict[file_name]


def commit_trunk_files(notes):
    trunk_path = _config.get('local_file_system', 'trunk_path')
    add(trunk_path + "/Resources")
    return commit(trunk_path, notes)


def commit_online_files(notes):
    online_path = _config.get('local_file_system', 'online_path')
    add(online_path + "/Resources")
    return commit(online_path, notes)


def update_all_files():
    trunk_path = _config.get('local_file_system', 'trunk_path')
    online_path = _config.get('local_file_system', 'online_path')
    update(trunk_path)
    update(online_path)


if __name__ == "__main__":
    # svnProcesser = SvnProcesser()
    # svnProcesser.merge_file_to_online(213718)
    # svnProcesser.update_all_files()
    # trunk_path = _config.get('local_file_system', 'trunk_path')
    # add(trunk_path)
    print "run svnProcesser"
