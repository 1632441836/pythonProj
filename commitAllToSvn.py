# -*- coding:utf-8 -*-
"""
提交文件至svn同时修改redmine状态
"""

import sys

from WorkTools import SvnProcesser as Svn
from WorkTools.RedmineProcesser import RedmineProcesser as Redmine

if __name__ == "__main__":
    print sys.argv
    issue_id = sys.argv[1]
    print issue_id
    redmine = Redmine('/issues/' + str(issue_id))
    Svn.update_all_files()
    redmine_note = redmine.get_svn_note()
    svn_revision = Svn.commit_trunk_files(redmine_note)
    redmine.change_issue_back_to_writer_and_state_done(svn_revision)
