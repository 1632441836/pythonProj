# -*- coding:utf-8 -*-

from WorkTools import DingRobot as DRobot
import ConfigParser
import os

_config = ConfigParser.ConfigParser()
_config.read(os.path.dirname(os.path.realpath(__file__)) + '/config.ini')

if __name__ == "__main__":
    test_robot_url = _config.get("remote_url", "ding_robot_test")
    test_reboot = DRobot.DingRobot(test_robot_url)
    test_reboot.send_text("hello")
