# -*- coding:utf-8 -*-

import commands
import os
from RelationStructure.RelationNet import RelationNet as RNet
import ConfigParser

LUA_KEYWORD = [
    "and", "break", "do", "else", "elseif", "end", "false", "for",
    "function", "if", "in", "local", "nil", "not", "or", "repeat",
    "return", "then", "true", "until", "while",
]

_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

BATTLE_FILE_LIST = []

BATTLE_FILE_PATH = _config.get("local_file_system", "battle_path")


if __name__ == "__main__":
    relation_net = RNet()

    battle_files = commands.getoutput("find " + BATTLE_FILE_PATH + " -name '*.lua'")
    file_list = battle_files.splitlines()

    for one_file in file_list:
        file_name = os.path.basename(one_file)
        module_name_list = file_name.split('.')
        BATTLE_FILE_LIST.append(module_name_list[0])
        relation_net.add_node(module_name_list[0])

    for one_file in file_list:
    # one_file = BATTLE_FILE_PATH + "/action/absorb/BAForAbsorbLogicAction.lua"
        file_name = os.path.basename(one_file)
        module_name_list = file_name.split('.')
        file_content = open(one_file, 'r').read()
        for module_name in BATTLE_FILE_LIST:
            if file_content.find(module_name) != -1:
                relation_net.add_relation(module_name_list[0], module_name)



    print "aaa"

    # print relation_net.draw_the_net()
    relation_net.draw_a_node("BattleModule")