import ConfigParser


# Set the third, optional argument of get to 1 if you wish to use raw mode.
class config:
    def __init__(self,config_name):
        self.config = ConfigParser.ConfigParser() #add exception if config not found
        self.config.read(config_name)
        self.jira_host=None
        self.jira_password = None
        self.jira_username = None
        self.delivery_team = None

    def get_access(self,access_section='access'):

        self.jira_host=self.config.get(access_section, 'jira_host')
        self.jira_password = self.config.get(access_section, 'jira_password')
        self.jira_username = self.config.get(access_section, 'jira_username')

    def get_settings(self, jira_section='jira_setttings'):
        self.delivery_team=self.config.get(jira_section, 'delivery_team')






