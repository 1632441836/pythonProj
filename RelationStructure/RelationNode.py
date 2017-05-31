# -*- coding:utf-8 -*-
"""
关系节点相关的类
"""

class RelationNode(object):
    """用于构建关系网节点的数据结构"""
    def __init__(self, value=""):
        self.__come_from = []
        self.__point_to = []
        self.__value = value

    def __str__(self):
        return self.__value

    def get_value(self):
        return self.__value

    def get_from_nodes(self):
        return self.__come_from

    def get_to_nodes(self):
        return self.__point_to

    def add_from_node(self, node_ins):
        if node_ins not in self.__come_from and node_ins.get_value() != self.get_value():
            self.__come_from.append(node_ins)
            node_ins.add_to_node(self)

    def add_to_node(self, node_ins):
        if node_ins not in self.__point_to and node_ins.get_value() != self.get_value():
            self.__point_to.append(node_ins)
            node_ins.add_from_node(self)

    def remove_from_node(self, node_ins):
        if node_ins in self.__come_from:
            self.__come_from.remove(node_ins)
            node_ins.remove_to_node(self)

    def remove_to_node(self, node_ins):
        if node_ins in self.__point_to:
            self.__point_to.remove(node_ins)
            node_ins.remove_from_node(self)

if __name__ == "__main__":
    cur_node = RelationNode("Hello")
    print cur_node
