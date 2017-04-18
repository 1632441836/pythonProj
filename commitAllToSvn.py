# -*- coding:utf-8 -*-

from RedmineProcesser import RedmineProcesser as Redmine
import SvnProcesser as Svn
import sys


if __name__ == "__main__":
    print sys.argv
    issue_id = sys.argv[1]
    print issue_id
    redmine = Redmine('/issues/' + str(issue_id))
    Svn.update_all_files()
    redmine_note = redmine.get_svn_note()
    svn_revision = Svn.commit_trunk_files(redmine_note)
    redmine.change_issue_back_to_writer_and_state_done(svn_revision)
