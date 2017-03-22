# This script shows how to use the client in anonymous mode
# against jiralib.atlassian.com.
from jiralib import jiralib,issueparser,reports
from config import Config
from optparse import OptionParser



parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")

parser.add_option("-c", "--config",
                  action="store",
                  dest="configpath",
                  default="jira.conf",
                  help="path to config file"
                 )
(options, args) = parser.parse_args()

conf = Config(options.configpath)
conf.get_access()
conf.get_settings()

myjira = jiralib.JiraLib(conf.jira_host,conf.jira_username,conf.jira_password,conf.component_name,conf.delivery_team)
myjira.connect()
myreport = reports.Reports(myjira)

print myreport.issue_in_statuses_in_days('PROD-1009', 'Design')
print myreport.issue_in_statuses_in_days('PROD-1009', 6)
