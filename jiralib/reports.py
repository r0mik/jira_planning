
import issueparser


class Reports:
    def __init__(self, jira_class):
        self.jira=jira_class

    def issue_in_statuses_in_days(self, issue, status):
        if type(status) != int:
            status=issueparser.status_to_int(status)
        time = 0
        latest_date = None
        issue = self.jira.get_issue_by_name(issue)
        trans = self.jira.get_issue_transitions(issue, status)
        for i in trans:
            for j in i:
                if i[j][0] == status:
                    time += int((j - latest_date).days)
                else:
                    latest_date = j

        return time
    def history_of_task(self, issue, status):
        if type(status) != int:
            status=issueparser.status_to_int(status)
        time = 0
        out={}
        latest_date = None
        issue = self.jira.get_issue_by_name(issue)
        trans = self.jira.get_issue_transitions(issue, status)
        for i in trans:
            for j in i:
                if i[j][0] == status:
                    time += int((j - latest_date).days)
                else:
                    latest_date = j


        return time