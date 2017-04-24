# -*- coding:utf-8 -*-
"""
文件映射map相关
"""
import os


def get_file_deepth(file_path):
    return len(file_path.split(os.path.sep))


class FileMap:
    """文件映射关系的map，使用一个map文件来创建，会对这个文件进行修改。"""
    def __init__(self):
        self.raw_file_string = ""
        self.file_map_list = []

    def add_relation(self, source_path, target_path):
        source_path = os.path.normpath(source_path)
        target_path = os.path.normpath(target_path)
        self.file_map_list.append((source_path, target_path, get_file_deepth(target_path)))
        self.file_map_list.sort(key=lambda x: x[2])

    def remove_relation(self, source_path, target_path):
        source_path = os.path.normpath(source_path)
        target_path = os.path.normpath(target_path)
        for tup in self.file_map_list:
            if tup[0] == source_path and tup[1] == target_path:
                self.file_map_list.remove(tup)

    def remove_all_relation(self):
        self.file_map_list = []

    def get_target_list(self, source_path):
        source_path = os.path.normpath(source_path)
        result_list = []
        for tup in self.file_map_list:
            if tup[0] == source_path:
                result_list.append(tup[1])
        return result_list

    def get_source_list(self, target_path):
        target_path = os.path.normpath(target_path)
        result_list = []
        for tup in self.file_map_list:
            if tup[1] == target_path:
                result_list.append(tup[0])
        return result_list

    def __convert_list_to_raw_string(self):
        raw_file = ""
        if self.file_map_list:
            for tup in self.file_map_list:
                raw_file += tup[0]
                raw_file += "-->"
                raw_file += tup[1]
                raw_file += '\n'
        return raw_file

    def __convert_raw_string_to_list(self):
        map_list = []
        if self.raw_file_string:
            raw_string_list = self.raw_file_string.splitlines()
            for line in raw_string_list:
                one_line_list = line.split("-->")
                if len(one_line_list) == 2:
                    map_list.append((one_line_list[0], one_line_list[1], get_file_deepth(one_line_list[1])))
        return map_list

    def read_ini_file(self, file_name="file_map.ini"):
        with open(file_name, 'r') as file_map:
            self.raw_file_string = file_map.read()
            self.file_map_list = self.__convert_raw_string_to_list()
            self.file_map_list.sort(key=lambda x: x[2])

    def write_back_file(self, file_name="file_map.ini"):
        with open(file_name, 'w') as file_map:
            file_map.write(self.__convert_list_to_raw_string())

    def __str__(self):
        show_string = "file map is:\n"
        for tup in self.file_map_list:
            show_string += tup[0]
            show_string += "-->"
            show_string += tup[1]
            show_string += '\n'
        return show_string


if __name__ == "__main__":
    f_map = FileMap()
    f_map.read_ini_file()
    print f_map
    f_map.add_relation('ccc', 'dddd')
    print f_map
    f_map.write_back_file()
