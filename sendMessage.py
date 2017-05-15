# -*- coding:utf-8 -*-
"""
钉钉机器人使用脚本
"""

from WorkTools import DingRobot as DRobot
import ConfigParser
import os

_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

if __name__ == "__main__":
    test_robot_url = _config.get("remote_url", "ding_robot_test")
    test_reboot = DRobot.DingRobot(test_robot_url)
    # test_reboot.send_text("hello")
    json = {
    "actionCard": {
        "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
        "text": """![screenshot](@lADOpwk3K80C0M0FoA)
 ### 乔布斯 20 年前想打造的苹果咖啡厅
 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划""",
        "hideAvatar": "1",
        "btnOrientation": "1",
        "singleTitle" : "阅读全文",
        "singleURL" : "https://www.dingtalk.com/"
    },
    "msgtype": "actionCard"
}

    json = {
    "actionCard": {
        "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
        "text": """![screenshot](@lADOpwk3K80C0M0FoA)
 ### 乔布斯 20 年前想打造的苹果咖啡厅
 Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划""",
        "hideAvatar": "0",
        "btnOrientation": "0",
        "btns": [
            {
                "title": "内容不错",
                "actionURL": "https://www.dingtalk.com/"
            },
            {
                "title": "不感兴趣",
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
    },
    "msgtype": "actionCard"
}
    test_reboot.post_request(json)
