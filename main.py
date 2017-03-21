# This script shows how to use the client in anonymous mode
# against jiralib.atlassian.com.
from jira import JIRA
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
print conf.delivery_team





