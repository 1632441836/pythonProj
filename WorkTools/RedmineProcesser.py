# -*- coding:utf-8 -*-
"""
redmine处理相关的类
"""

import cookielib
import requests
from bs4 import BeautifulSoup
import re
import ConfigParser
import os


class PostData:
    """用于发送的字典"""
    __dictionary = {}
    __config = ConfigParser.ConfigParser()

    def __init__(self):
        self.__dictionary = {}
        self.__config.read(os.path.dirname(os.path.realpath(__file__)) + '/../config.ini')
        self.__dictionary['authenticity_token'] = self.__config.get('network_info', 'authenticity_token')
        self.__dictionary['_method'] = "put"

    def add_issue_assign_to(self, assign_to):
        if assign_to:
            self.__dictionary['issue[assigned_to_id]'] = assign_to

    def add_notes(self, notes):
        if notes:
            self.__dictionary['notes'] = notes

    def add_issue_status(self, status):
        if status:
            self.__dictionary['issue[status_id]'] = status

    def get_dictionary(self):
        return self.__dictionary


class RedmineProcesser:
    """用于处理redmine的class, 基于requests"""
    __opener = None
    __page_soup = None
    __session = None
    __issue_locate = ''
    __redmine_url = ''
    __sub_issue_list = []
    __svn_revision_list = []
    __assigned_to = ''
    __config = ConfigParser.ConfigParser()

    def __init__(self, issue_locate):
        self.__config.read(os.path.dirname(os.path.realpath(__file__)) + '/../config.ini')
        # 补充几个config中的内容
        self.__redmine_url = self.__config.get('network_info', 'redmine_url')
        # 本redmine问题地址
        self.__issue_locate = issue_locate
        # 创建cookies对象
        cookie = cookielib.MozillaCookieJar()
        cookie.load(os.path.dirname(os.path.realpath(__file__)) + '/../cookie.txt', True, True)
        # 构建headers的基础内容
        headers = {
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "max-age=0",
            "User-agent": self.__config.get('network_info', 'User-agent')
        }

        # 创建窗口
        self.__session = requests.Session()
        self.__session.cookies = cookie
        self.__session.headers = headers

        # 发送网络请求获取网页内容
        try:
            response = self.__session.get(self.__get_issue_url())
            html = response.content
            self.__page_soup = BeautifulSoup(html, "html.parser")
            self.__sub_issue_list = self.__get_all_sub_issue()
            self.__svn_revision_list = self.__get_all_svn_revision()
            self.__assigned_to = self.__get_issue_assigned_to()
        except Exception as e:
            print 'redmine init error'
            print e
            raise

    def __get_issue_url(self):
        return self.__redmine_url + self.__issue_locate

    def __get_all_sub_issue(self):
        sub_issue_list = [self.__issue_locate]
        sub_issue_table = self.__page_soup.find(name='div', id='issue_tree')
        if sub_issue_table.form is not None:
            sub_issue_subject = sub_issue_table.form.table.find_all(href=re.compile('/issues/*'))
            for subjectName in sub_issue_subject:
                sub_issue_list.append(subjectName.get('href'))
        return sub_issue_list

    def __get_all_svn_revision(self):
        result = []
        history = self.__page_soup.find(name='div', id='history')
        if history:
            for one_his in history.find_all('p'):
                if one_his.getText().find('pid') == -1 and one_his.getText().find(u'已合并') == -1:
                    match = re.findall(r'\d{3},?\d{3}', one_his.getText())
                    for revision_str in match:
                        result.append(filter(str.isdigit, revision_str.encode('ascii')))
        return result

    def __split_userid_from_raw_userstring(self, user_string):
        if user_string:
            match = re.findall('/users/(\d*)', user_string)
            if match:
                return match[0]
        return ''

    def __get_issue_assigned_to(self):
        assign_locate = ""
        for assignTo in self.__page_soup.find_all(name='td', class_='assigned-to'):
            if assignTo.a:
                assign_locate = assignTo.a['href']
        return assign_locate

    def __get_issue_writer(self):
        writer = ""
        for assignTo in self.__page_soup.find_all(name='p', class_='author'):
            writer = assignTo.a['href']
        return writer

    def __get_issue_assigned_to_id(self):
        return self.__split_userid_from_raw_userstring(self.__get_issue_assigned_to())

    def __get_issue_writer_id(self):
        return self.__split_userid_from_raw_userstring(self.__get_issue_writer())

    def __is_my_issue(self):
        return self.__assigned_to == '/users/' + self.__config.get('user_id', 'my_id')

    def sub_issue_list(self):
        return self.__sub_issue_list

    def svn_revision_list(self):
        return self.__svn_revision_list

    def change_state(self, assign_to=None, note=None, status=None):
        post_data = PostData()
        post_data.add_notes(note)
        post_data.add_issue_assign_to(assign_to)
        post_data.add_issue_status(status)

        try:
            response = self.__session.post(self.__get_issue_url(), post_data.get_dictionary())
            if response.ok:
                print self.__issue_locate + ":ok"
        except Exception as e:
            print e
            print self.__issue_locate
            return 1
        return 0

    def change_issue_to_qa_and_state_feedback(self, note):
        qa_id = self.__config.get('user_id', 'qa')
        if self.__is_my_issue():
            status = self.__config.get('issue_status', 'feedback')
        else:
            status = ""
        self.change_state(qa_id, note, status)

    def change_issue_back_to_writer_and_state_done(self, note):
        if self.__is_my_issue():
            assign_to_id = self.__get_issue_writer_id()
        else:
            assign_to_id = self.__get_issue_assigned_to_id()
        status = self.__config.get('issue_status', 'solved')
        self.change_state(assign_to_id, note, status)

    def get_svn_note(self):
        subject_node = self.__page_soup.find(name='div', class_='subject')
        subject_string = subject_node.div.h3.string

        page_node = self.__page_soup.find(name='div', id='content')
        number_string = page_node.h2.string

        return number_string + ' ' + subject_string


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    redmine = RedmineProcesser('/issues/42022')
    # print redmine.get_svn_note()
    # print redmine.svn_revision_list()
    # print redmine.get_issue_writer()
