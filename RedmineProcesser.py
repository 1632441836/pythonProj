# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import re
import ConfigParser


class PostData:
    """用于发送的字典"""
    __dictionary = {}
    __config = ConfigParser.ConfigParser()

    def __init__(self):
        self.__dictionary = {}
        self.__config.read('config.ini')
        self.__dictionary['authenticity_token'] = self.__config.get('network_info', 'authenticity_token')
        self.__dictionary['_method'] = "put"

    def add_issue_assign_to(self, assign_to):
        self.__dictionary['issue[assigned_to_id]'] = assign_to

    def add_notes(self, notes):
        self.__dictionary['notes'] = notes

    def add_issue_state(self, state):
        self.__dictionary['issue[status_id]'] = state

    def get_dictionary(self):
        return self.__dictionary


class RedmineProcesser:
    """用于处理redmine的class"""
    __opener = None
    __page_soup = None
    __issue_locate = ''
    __redmine_url = ''
    __sub_issue_list = []
    __svn_revision_list = []
    __assigned_to = ''
    __headers = {
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "max-age=0"
    }
    __config = ConfigParser.ConfigParser()

    def __init__(self, issue_locate):
        self.__config.read('config.ini')
        # 补充几个config中的内容
        self.__redmine_url = self.__config.get('network_info', 'redmine_url')
        self.__headers['User-agent'] = self.__config.get('network_info', 'User-agent')
        # 本redmine问题地址
        self.__issue_locate = issue_locate
        # 创建带cookie的opener
        cookie = cookielib.MozillaCookieJar()
        cookie.load('cookie.txt', True, True)
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # 发送网络请求获取网页内容
        try:
            request = urllib2.Request(self.__get_issue_url(), headers=self.__headers)
            response = self.__opener.open(request)
            html = response.read()
            self.__page_soup = BeautifulSoup(html, "html.parser")
            self.__sub_issue_list = self.__get_all_sub_issue()
            self.__svn_revision_list = self.__get_all_svn_revision()
            self.__assigned_to = self.__get_issue_assigned_to()
        except Exception as e:
            print 'redmine init error'
            print e

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
                if one_his.getText().find('pid') == -1:
                    match = re.findall(r'\d{3},?\d{3}', one_his.getText())
                    for revision_str in match:
                        result.append(filter(str.isdigit, revision_str.encode('ascii')))
        return result

    def __get_issue_assigned_to(self):
        assign_locate = ""
        for assignTo in self.__page_soup.find_all(name='td', class_='assigned-to'):
            assign_locate = assignTo.a['href']
        return assign_locate

    def __is_my_issue(self):
        return self.__assigned_to == '/users/' + self.__config.get('user_id', 'my_id')

    def sub_issue_list(self):
        return self.__sub_issue_list

    def svn_revision_list(self):
        return self.__svn_revision_list

    def change_state(self, assign_to, note):
        post_data = PostData()
        post_data.add_notes(note)
        if self.__is_my_issue():
            post_data.add_issue_assign_to(assign_to)

        # print self.__issue_locate
        # print post_data.get_dictionary()

        try:
            encode_post_data = urllib.urlencode(post_data.get_dictionary())
            request = urllib2.Request(self.__get_issue_url(), encode_post_data, headers=self.__headers)
            response = self.__opener.open(request)
            print response.getcode()
        except Exception as e:
            print e
            print self.__issue_locate
            return 1
        return 0

    def get_svn_note(self):
        subject_node = self.__page_soup.find(name='div', class_='subject')
        subject_string = subject_node.div.h3.string

        page_node = self.__page_soup.find(name='div', id='content')
        number_string = page_node.h2.string

        return number_string + ' ' + subject_string


if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    redmine = RedmineProcesser('/issues/41529')
    # redmine.change_state(config.get('user_id', 'qa'), 'test')
    print redmine.get_svn_note()
