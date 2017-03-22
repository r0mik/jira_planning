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
"""
from jiralib_old import JIRA
from issueparser import parse_descriptions,errors_to_strings, status_to_int, priority_to_int

#add documentation
#
#

class jiratask:
    def __init__(self, server_name, user, password, component ='Infrastructure',delivery_team='Infra build'):
        self.server=server_name
        self.user=user
        self.password=password
        self.jira=None
        self.delivery_team=delivery_team
        self.component = component

class myjira:
    def __init__(self, server_name, user, password, component ='Infrastructure',delivery_team='Infra build'):
        self.server=server_name
        self.user=user
        self.password=password
        self.jira=None
        self.delivery_team=delivery_team
        self.component = component

    def set_delivery_team(self,name):
        self.delivery_team=name

    def connect(self):

        options = Infrastructure
            'server': self.server
        }
        self.jira = JIRA(options,basic_auth=(self.user, self.password))# This script shows how to use the client in anonymous mode
# against jiralib.atlassian.com.
from jiralib_old import JIRA
import re

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
options = {
    'server': 'https://jiralib.atlassian.com'}
jira = JIRA(options)

# Get all projects viewable by anonymous users.
projects = jira.projects()

# Sort available project keys, then return the second, third, and fourth keys.
keys = sorted([project.key for project in projects])[2:5]

# Get an issue.
issue = jira.issue('JRA-1330')

# Find all comments made by Atlassians on this issue.
atl_comments = [comment for comment in issue.fields.comment.comments
                if re.search(r'@atlassian.com$', comment.author.emailAddress)]


    def search_issues(self,qery):
        return self.jira.search_issues(qery)

    def get_issue_by_name(self,issue_name):
        return self.jira.issue(issue_name)

    def get_all_epic(self,anddone=None):
        if anddone:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND type = Epic'% (self.component,self.delivery_team)
        else:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND status != Done AND type = Epic'% (self.component,self.delivery_team)
        return self.search_issues(qery)

    def get_all_us(self,anddone=None):
        if anddone:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND type = "User Story"'% (self.component,self.delivery_team)
        else:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND status != Done AND type = "User Story"'% (self.component,self.delivery_team)
        return self.search_issues(qery)

    def get_all_us_in_epic(self,issue,anddone=None):
        #customfield_11701
        if anddone:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND type = "User Story" AND "Epic Link" = "%s"'% (self.component,self.delivery_team,str(issue.fields.customfield_11701))
        else:
            qery='project = PROD AND component =  %s AND "Delivery team" = "%s" AND status != Done AND type = "User Story" AND "Epic Link" = "%s"'% (self.component,self.delivery_team,str(issue.fields.customfield_11701))
        return self.search_issues(qery)

    def check_epic (self, issue):
        out=[]
        out.append(self.parse_desc(issue.fields.description)) #move to separate epic from 3 level (only after scoping)
        out.append(self.check_issue_responsible_manager(issue))
        out.append(self.check_epic_design_document(issue))
        out.append(self.check_epic_product_manager(issue))
        out.append(self.check_epic_health(issue))
        out.append(self.check_epic_fixversion(issue))
        out.append(self.check_epic_status(issue))
        out.append(self.check_epic_qa(issue))
        out.append(self.check_epic_blueprint(issue))
        for i in range(out.count(0)):
            out.remove(0)
        return out

    def check_us(self,issue):
        out=[]
        out.append(self.parse_desc(issue.fields.description)) #move to separate epic from 3 level in Epic
        #out.append(self.check_issue_responsible_manager(issue))
        out.append(self.check_us_design_document(issue))
        out.append(self.check_us_fixversion(issue))
        for i in range(out.count(0)):
            out.remove(0)
        return out

    def check_issue_responsible_manager(self, issue):
        if issue.fields.customfield_16826:
            return 0
        else:
            return 4

    def check_epic_design_document(self,issue):
        if (self.get_the_status_int(issue) in [5,6,7,8]) and not (issue.fields.customfield_16803) :
            return 5
        return 0

    def check_epic_blueprint(self,issue):
        if (self.get_the_status_int(issue) in [5,6,7,8]) and not (issue.fields.customfield_16802) and (self.get_issue_iso_codebase(issue)=='Yes'):
            return 14
        return 0

    def check_epic_health(self,issue):
        if (self.get_the_status_int(issue) in [5,6,7,8]) and not (issue.fields.customfield_16909):
            return 6
        return 0

    def check_epic_product_manager(self,issue):
        if (self.get_the_status_int(issue) in [5,6,7,8]) and not (issue.fields.customfield_16800):
            return 9
        return 0


    def check_epic_fixversion(self,issue):
        if (self.get_the_status_int(issue) in [4,5,6,7,8]) and not (issue.fields.fixVersions):
            return 7
        if (self.get_the_status_int(issue) in [1,2,3]) and  (issue.fields.fixVersions):
            return 8
        return 0

    def check_us_fixversion(self,issue):
        epic_name=self.get_epic_from_us(issue)
        if not epic_name:
            return 13
        epic_status =self.get_the_status_int(epic_name)

        if epic_status in [4,5,6,7,8] and not (issue.fields.fixVersions):
            return 7
        return 0

    def check_us_design_document(self,issue):
        epic_name=self.get_epic_from_us(issue)
        if not epic_name:
            return 13
        if str(self.get_the_summary(issue)).find('design document') >=0 and not (issue.fields.customfield_16803) and \
                ( self.get_the_status_int(epic_name) in [5,6,7] ):
            return 5
        return 0



    def check_epic_status(self,issue):
        status=self.get_the_status_int(issue)
        if status < 4 :
            return 0

        us=self.get_epic_subtasks(issue)
        us_status=[]
        for i in us:
            us_status.append(self.get_the_status_int(i))

        if status >4 and not us:
            return 11
        if status == 6 and (1 not in us_status) and (6 not in us_status) and (7 not in us_status):
            return 10
        return 0

    def check_epic_qa(self,issue):
        if str(self.get_issue_iso_codebase(issue)) == 'Yes' and self.get_the_status_int(issue) == 7 and not self.get_qa_eng(issue):
            return 12
        return 0

    def epic_problem_to_trello(self,issue):
        out=[]
        status=self.get_the_status_int(issue)
        for i in self.return_epic_conclusion(issue):
            out.append({'Assign':self.get_issue_assignee(issue),
                        'Name': '['+str(issue)+'] '+ str(i),
                        'Description': 'EPIC name: '+str(self.get_the_summary(issue))+'\nProblem:'+str(i)+'\nAssignee: '+self.get_issue_assignee(issue),
                        'Url': self.server+'/browse/'+str(issue),
                        'Status':status
                        })
        return out
    def us_problem_to_trello(self,issue):
        out=[]
        status=self.get_the_status_int(issue)
        for i in self.return_us_conclusion(issue):
            out.append({'Assign':self.get_issue_assignee(issue),
                        'Name': '['+str(issue)+'] '+ str(i),
                        'Description': 'US Name: '+str(self.get_the_summary(issue))+'\nProblem: '+str(i)+'\nAssignee: '+self.get_issue_assignee(issue),
                        'Url': self.server+'/browse/'+str(issue),
                        'Status':status
                        })
        return out

    def return_epic_conclusion(self,issue):
        return self.return_conclusion(self.check_epic(issue))

    def return_us_conclusion(self,issue):
        return self.return_conclusion(self.check_us(issue))

    def parse_desc(self,desc):
        return parse_descriptions(desc)


    def return_conclusion(self,list_of_error):
        out=[]
        for i in list_of_error:
            out.append(errors_to_strings(i))
        return out

    def get_the_status_text(self,issue):
        return str(issue.fields.status)

    def get_the_status_int(self,issue):
        return status_to_int(str(issue.fields.status))

    def get_priority_text(self,issue):
        return str(issue.fields.priority)

    def get_priority_int(self,issue):
        return priority_to_int(str(issue.fields.priority))

    def get_epic_healts(self,issue):
        return str(issue.fields.customfield_16909)

    def get_epic_subtasks(self,issue):
        return self.get_all_us_in_epic(issue,1)

    def get_qa_eng(self,issue):
        return str(issue.fields.customfield_17101)

    def get_issue_iso_codebase(self,issue):
        return str(issue.fields.customfield_18208)

    def get_the_summary(self,issue):
        return issue.fields.summary

    def get_epic_from_us(self,issue):
        if issue.fields.customfield_11700:
            return self.get_issue_by_name(issue.fields.customfield_11700)
        return None

    def get_issue_assignee(self,issue):
        if issue.fields.assignee:
            return issue.fields.assignee.displayName
        else:
            #print str(issue)+'Name not found'
            return 'Not Assigned'

    def get_issue_attachment(self,issue):
        return issue.fields.issuelinks


# check bp in EPIC if affecting iso
# check initiative
# card for demo
# card for publish