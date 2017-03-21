from jiralib import JIRA

class JiraLib:
    def __init__(self):
        self, server_name, user, password, component = 'Infrastructure', delivery_team = 'MOS Infra'):
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