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

    print 'revision numbers:'

    for revision in revisionList:
        print revision,

    print 'update the files'

    svn.update_all_files()

    print 'merge the files'

    for revision in revisionList:
        svn.copy_file_to_online(revision)

    print 'please check the files manually'
    print 'commit or not?(y/n)'

    commit = raw_input()
    if commit == 'y':
        svn.commit_online_files(redmineRoot.get_svn_note())

    print 'input the note'

    note = raw_input()

    for redmine in redmineList:
        redmine.change_state(config.get('user_id', 'qa'), note)
