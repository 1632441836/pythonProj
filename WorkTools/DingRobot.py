# -*- coding:utf-8 -*-
"""
钉钉机器人相关的类
"""

import requests


class RobotJson:
    """
    钉钉机器人使用的json格式
    """
    def __init__(self):
        self.msg = {}

    def __str__(self):
        return self.msg

    def get_json(self):
        print self.msg
        return self.msg


class NormalTextJson(RobotJson):
    """
    普通格式，可以at
    """
    def __init__(self):
        RobotJson.__init__(self)
        self.msg = {
            "msgtype": "text",
            "text": {
                "content": ""
            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }

    def add_content(self, content):
        self.msg["text"]["content"] = content

    def add_at_mobile(self, mobile_phone):
        self.msg["at"]["atMobiles"].append(mobile_phone)

    def at_all(self, b_at_all):
        if b_at_all:
            self.msg["at"]["atMobiles"] = []
        self.msg["at"]["isAtAll"] = b_at_all


class LinkJson(RobotJson):
    """
    链接格式
    """
    def __init__(self):
        RobotJson.__init__(self)
        self.msg = {
            "msgtype": "link",
            "link": {
                "text": "",
                "title": "",
                "picUrl": "",
                "messageUrl": ""
            }
        }

    def add_text(self, text):
        self.msg["link"]["text"] = text

    def add_title(self, title):
        self.msg["link"]["title"] = title

    def add_pic_url(self, pic_url):
        self.msg["link"]["picUrl"] = pic_url

    def add_message_url(self, message_url):
        self.msg["link"]["messageUrl"] = message_url


class MarkdownJson(RobotJson):
    """
    markdown格式

    标题
    # 一级标题
    ## 二级标题
    ### 三级标题
    #### 四级标题
    ##### 五级标题
    ###### 六级标题

    引用
    > A man who stands for nothing will fall for anything.

    文字加粗、斜体
    **bold**
    *italic*

    链接
    [this is a link](http://name.com)

    图片
    ![](http://name.com/pic.jpg)

    无序列表
    - item1
    - item2

    有序列表
    1. item1
    2. item2
    """
    def __init__(self):
        RobotJson.__init__(self)
        self.msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": "",
                "text": ""
            }
        }

    def add_title(self, title):
        self.msg["markdown"]["title"] = title

    def add_text(self, text):
        self.msg["markdown"]["text"] = text


class DingRobot:
    """钉钉机器人"""
    def __init__(self, robot_url):
        self.__robot_url = robot_url

    def post_request(self, post_json):
        response = requests.post(self.__robot_url, json=post_json)
        print response.content

    def send_text(self, text):
        send_data = NormalTextJson()
        send_data.add_content(text)
        self.post_request(send_data.get_json())

    def send_markdown(self, markdown_title, markdown_text):
        send_data = MarkdownJson()
        send_data.add_title(markdown_title)
        send_data.add_text(markdown_text)
        self.post_request(send_data.get_json())

    def send_link(self, text, title, pic_url, message_url):
        send_data = LinkJson()
        send_data.add_text(text)
        send_data.add_title(title)
        send_data.add_pic_url(pic_url)
        send_data.add_message_url(message_url)
        self.post_request(send_data.get_json())

if __name__ == "__main__":
    print "dingRobot"
