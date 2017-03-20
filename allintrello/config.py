import ConfigParser


# Set the third, optional argument of get to 1 if you wish to use raw mode.
class config:
    def __init__(self,config_name):
        self.config = ConfigParser.ConfigParser() #add exception if config not found
        self.config.read(config_name)
        self.jira_host=None
        self.jira_password = None
        self.jira_name = None
        self.trello_key = None
        self.trello_token = None
        self.board_id = None
        self.backlog_list = None
        self.todo_list = None
        self.inprogress_list = None


    def get_access(self,access_section='access'):

        self.jira_host=self.config.get(access_section, 'jira_host')
        self.jira_password = self.config.get(access_section, 'jira_password')
        self.jira_name = self.config.get(access_section, 'jira_name')
        self.trello_key = self.config.get(access_section, 'trello_key')
        self.trello_token = self.config.get(access_section, 'trello_token')

    def get_trello(self, trello_section='trello'):
        self.board_id=self.config.get(trello_section, 'board_id')
        self.backlog_list = self.config.get(trello_section, 'backlog_list')
        self.todo_list = self.config.get(trello_section, 'todo_list')
        self.inprogress_list = self.config.get(trello_section, 'inprogress_list')






