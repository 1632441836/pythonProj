# -*- coding:utf-8 -*-

import urllib, urllib2
import cookielib
from bs4 import BeautifulSoup
import re
import ConfigParser

class PostData:
    '用于发送的字典'
    __dictionary = {}
    __config = ConfigParser.ConfigParser()

    def __init__(self):
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
    '用于处理redmine的class'
    __opener = None
    __page_soup = None
    __issue_locate = ''
    __redmine_url = ''
    __sub_issue_list = []
    __svn_revision_list = []
    __assigned_to = ''
    __headers = {
        "Connection":"keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control":"max-age=0"
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
        request = urllib2.Request(self.__get_issue_url(), headers=self.__headers)
        response = self.__opener.open(request)
        html = response.read()
        self.__page_soup = BeautifulSoup(html, "html.parser")
        self.__sub_issue_list = self.__get_all_sub_issue()
        self.__svn_revision_list = self.__get_all_svn_revision()
        self.__assigned_to = self.__get_issue_assigned_to()

    def __get_issue_url(self):
        return self.__redmine_url + self.__issue_locate

    def __get_all_sub_issue(self):
        subIssueList = [self.__issue_locate]
        subIssueTable = self.__page_soup.find_all(id='issue_tree')
        for result in subIssueTable:
            if (result.form != None):
                subIssueSubject = result.form.table.find_all(href=re.compile('/issues/*'))
                for subjectName in subIssueSubject:
                    subIssueList.append(subjectName.get('href'))
        return subIssueList

    def __get_all_svn_revision(self):
        result = []
        history = self.__page_soup.find_all(id='history')
        for his in history:
            for one_his in his.find_all('p'):
                if (one_his.getText()):
                    match = re.search(r'\d{3},?\d{3}', one_his.getText())
                    if (match):
                        result.append(filter(str.isdigit, match.group().encode('ascii')))
        return result

    def __get_issue_assigned_to(self):
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
        postData = PostData()
        postData.add_notes(note)
        if self.__is_my_issue():
            postData.add_issue_assign_to(assign_to)

        try:
            request = urllib2.Request(self.__get_issue_url(), urllib.urlencode(postData.get_dictionary()), headers=self.__headers)
            response = self.__opener.open(request)
        except Exception as e:
            print e
            print self.__issue_locate
            return 1
        return 0

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    redmine = RedmineProcesser('/issues/41529')
    redmine.change_state(config.get('user_id', 'qa'), 'test')


