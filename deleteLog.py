# -*- coding:utf-8 -*-

import sys
import os

flag_list = ["TimeUtil.timeStart",
             "logger:debug",
             "TimeUtil.timeEnd",
             "print_table",
             "Logger.debug",
             "print_t",
             "print"]
file_ignore_list = ["Logger.lua",
                    "LuaUtil.lua"]


def calculate_end_pos(start_p, cur_flag, calculate_string):
    # 先向后移动游标到flag之后
    start_p += len(cur_flag)

    while calculate_string[start_p] != "(":
        if calculate_string[start_p] == ' ' or calculate_string[start_p] == '\n' or calculate_string[start_p] == '\t':
            start_p += 1
        else:
            # 这种情况说明不是需要删除的log的情况
            print "*******************"
            print "这块这个没删"
            print file_path
            print start_p
            print cur_flag
            print calculate_string[start_p]
            print "*******************"
            return -1

    start_p += 1
    end_p = start_p
    bracket_num = 1

    while bracket_num > 0:
        if calculate_string[end_p] == "(":
            bracket_num += 1
        if calculate_string[end_p] == ")":
            bracket_num -= 1
        end_p += 1

    return end_p

if __name__ == "__main__":
    file_path = sys.argv[1]
    print file_path

    # 跳过忽略列表
    if os.path.basename(file_path) in file_ignore_list:
        print "*******************"
        print "this file has been ignored."
        print file_path
        print "*******************"
        exit(0)

    # 读入文件
    lua_file = open(file_path, 'r+')
    file_content = lua_file.read()
    lua_file.close()

    file_find_start = 0
    for flag in flag_list:
        while True:
            start_pos = file_content.find(flag, file_find_start)
            if start_pos == -1:
                file_find_start = 0
                break
            end_pos = calculate_end_pos(start_pos, flag, file_content)
            # 有时可能会搜索到形如printLog这种字符串，这种字符串在上面的计算结束点的函数中会得到判断并返回-1，通过确定搜索范围来跳过这个。
            if end_pos != -1:
                print file_content[start_pos:end_pos]
                file_content = file_content[0:start_pos] + file_content[end_pos:len(file_content)]
                file_find_start = start_pos
            else:
                file_find_start = start_pos + len(flag)

    # 写回文件
    lua_file = open(file_path, "w+")
    lua_file.write(file_content)
    lua_file.close()
