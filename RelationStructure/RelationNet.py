# -*- coding:utf-8 -*-
"""
关系网相关的类
"""

from RelationNode import RelationNode as RNode
import pydot
import ConfigParser
import os


_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/../config.ini')


class RelationNet:
    """关系网的类"""
    def __init__(self):
        self.__cur_node = None
        self.__head_node = None
        self.__node_map = {}
        self.__draw_nodes = []
        self.__relation_map = {}
        self.__node_num = 0

    def add_node(self, node_name):
        node_ins = RNode(node_name)
        self.__cur_node = node_ins
        if not self.__head_node:
            self.__head_node = node_ins
        self.__node_num += 1
        if node_name not in self.__node_map:
            self.__node_map[node_name] = node_ins

    def get_node(self, node_name):
        if node_name in self.__node_map:
            return self.__node_map[node_name]

    def __add_to_draw_nodes(self, node_ins):
        if node_ins not in self.__draw_nodes:
            self.__draw_nodes.append(node_ins)

    def add_relation(self, from_node_name, to_node_name):
        from_node_ins = self.get_node(from_node_name)
        to_node_ins = self.get_node(to_node_name)
        if from_node_ins and to_node_ins:
            from_node_ins.add_to_node(to_node_ins)
            self.__add_to_draw_nodes(from_node_ins)
            self.__add_to_draw_nodes(to_node_ins)

    def draw_the_net(self):
        """use pydot"""
        g = pydot.Dot("battle analysis", graph_type="digraph")

        for value in self.__draw_nodes:
            node = pydot.Node(value.get_value(), label=value.get_value())
            g.add_node(node)

        for value in self.__node_map.values():
            for to_node in value.get_to_nodes():
                edge = pydot.Edge(value.get_value(), to_node.get_value())
                g.add_edge(edge)

        g.write(_config.get("local_file_system", "test_tmp_file") + "/battle.jpg", prog="dot", format="jpg")
        return g.to_string()

    def draw_a_node(self, node_name):
        g = pydot.Dot("battle analysis", graph_type="digraph")

        node_ins = self.__node_map[node_name]
        dot_node = pydot.Node(node_ins.get_value(), label=node_ins.get_value())
        g.add_node(dot_node)
        for node in node_ins.get_to_nodes():
            dot_node = pydot.Node(node.get_value(), label=node.get_value())
            g.add_node(dot_node)
            dot_edge = pydot.Edge(node.get_value(), node_ins.get_value())
            g.add_edge(dot_edge)

        for node in node_ins.get_from_nodes():
            dot_node = pydot.Node(node.get_value(), label=node.get_value())
            g.add_node(dot_node)
            dot_edge = pydot.Edge(node_ins.get_value(), node.get_value())
            g.add_edge(dot_edge)

        g.write(_config.get("local_file_system", "test_tmp_file") + "/battle.jpg", prog="dot", format="jpg")
        return g.to_string()

    def __str__(self):
        show_net = ""
        for value in self.__node_map.values():
            show_net += "-------"
            show_net += value.get_value()
            show_net += "-------"
            show_net += '\n'
            for to_node in value.get_to_nodes():
                show_net += value.get_value()
                show_net += "-->"
                show_net += to_node.get_value()
                show_net += '\n'
            show_net += '\n'
        return show_net

    def __len__(self):
        return self.__node_num

if __name__ == "__main__":
    RNet = RelationNet()
    RNet.add_node("aaa")
    RNet.add_node("bbb")
    RNet.add_relation("aaa", "bbb")
    print RNet.draw_the_net()
