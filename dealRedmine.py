# -*- coding:utf-8 -*-

from RedmineProcesser import RedmineProcesser as Redmine
from SvnProcesser import SvnProcesser as Svn
import ConfigParser

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    svn = Svn()
    config.read('config.ini')
    print 'please input redmine number:'
    issueNumber = raw_input()
    redmineRoot = Redmine('/issues/'+str(issueNumber))
    redmineList = []
    revisionList = []
    for issueLocate in redmineRoot.sub_issue_list():
        redmine = Redmine(issueLocate)
        redmineList.append(redmine)
        for revision in redmine.svn_revision_list():
            if revision not in revisionList:
                revisionList.append(revision)

    print 'revision numbers:\n'

    for revision in revisionList:
        svn.copy_file_to_online(revision)
        print revision,

    print '\n'

    print 'merge the code and input the note\n'

    note = raw_input()

    for redmine in redmineList:
        redmine.change_state(config.get('user_id', 'qa'), note)

