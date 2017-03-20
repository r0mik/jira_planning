# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
from jira import JIRA
import re

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
options = {
    'server': 'https://mirantis.jira.com'
    }
jira = JIRA(options, basic_auth=())

# Get all projects viewable by anonymous users.
projects = jira.projects()


# Get an issue.
issue = jira.issue('PROD-9541')

print issue.fields.summary