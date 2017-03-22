"""
custom fields
customfield_16826 :responsible manager
customfield_16802: blueprint
customfield_18208: iso code base
customfield_17101:QA eng
customfield_16800: product manager
customfield_17102: sw eng
customfield_17100: design reviewers
customfield_16803: design document
customfield_16909: health
customfield_11701: epic name
customfield_11700: epic link
customfield_10423: epic link
"""

from jira import JIRA
import issueparser
from datetime import datetime

class JiraLib:
    def __init__(self, server_name, user, password, component = 'Infrastructure', delivery_team = 'MOS Infra'):
        self.server = server_name
        self.user = user
        self.password = password
        self.jira = None
        self.delivery_team = delivery_team
        self.component = component

    def connect(self):
        options = {
            'server': self.server
        }
        self.jira = JIRA(options, basic_auth=(self.user, self.password))

    def get_all_epic(self,anddone=None):
        if anddone:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND type = Epic'% (self.component,self.delivery_team)
        else:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND status != Done AND type = Epic'% (self.component,self.delivery_team)
        return self.search_issues(qery)

    def search_issues(self,qery):
        return self.jira.search_issues(qery, expand='changelog')

    def get_all_us_in_epic(self,issue,anddone=None):
        #customfield_11701
        if anddone:
            qery='project = PROD AND type = "User Story" AND "Epic Link" = "%s"'% (str(issue.fields.customfield_11701))
        else:
            qery='project = PROD AND status != Done AND type = "User Story" AND "Epic Link" = "%s"'% (str(issue.fields.customfield_11701))
        return self.search_issues(qery)

    def get_issue_by_name(self,issue_name):
        return self.jira.issue(issue_name, expand='changelog')

    def get_issue_transitions_in_progress(self, issue):
        out=[]
        for history in issue.changelog.histories:
            for item in history.items:
                # Fixme: workaround for timezone
                timezone = '-' + str(history.created.rsplit('-', 1)[1])
                if item.field == 'status' and (issueparser.status_to_int(item.toString) in [6] or
                                                   issueparser.status_to_int(item.fromString) in [6]):

                    out.append({datetime.strptime(history.created, '%Y-%m-%dT%H:%M:%S.%f'+timezone):
                                    [issueparser.status_to_int(item.fromString),
                                    issueparser.status_to_int(item.toString)]})
        return out

    def get_issue_transitions_in_design(self, issue):
        out = []
        for history in issue.changelog.histories:
            for item in history.items:
                # Fixme: workaround for timezone
                timezone='-'+str(history.created.rsplit('-', 1)[1])
                if item.field == 'status' and (issueparser.status_to_int(item.toString) in [5] or
                                                       issueparser.status_to_int(item.fromString) in [5]):
                    out.append({datetime.strptime(history.created, '%Y-%m-%dT%H:%M:%S.%f'+timezone):
                                    [issueparser.status_to_int(item.fromString),
                                    issueparser.status_to_int(item.toString)]})
        return out

    def get_issue_transitions(self, issue, status):
        out = []
        for history in issue.changelog.histories:
            for item in history.items:
                # Fixme: workaround for timezone
                timezone = '-' + str(history.created.rsplit('-', 1)[1])
                if item.field == 'status' and (issueparser.status_to_int(item.toString) in [status] or
                                                       issueparser.status_to_int(item.fromString) in [status]):
                    out.append({datetime.strptime(history.created, '%Y-%m-%dT%H:%M:%S.%f' + timezone):
                                    [issueparser.status_to_int(item.fromString),
                                     issueparser.status_to_int(item.toString)]})
        return out