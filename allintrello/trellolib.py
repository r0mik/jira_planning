from trello import TrelloApi
trello = TrelloApi('afc78d3af06d03c9a9cd035dee2fc757','583ad6c89f03effe7fe14173720a4813effb21f642ff0f73bc0c63ee2c63a386') #hardcode
lists=trello.boards.get_list('eZmHpRt0') #hardcoded lists

class mytrello:
    def __init__(self,apikey,token,boardname,lowprioritylist,hightprioritylist,criticalprioritylist):
        self.apikey=apikey
        self.token=token
        self.boardname=boardname
        self.todo =None
        self.backlog=None
        self.inprogress=None
        self.trello=None
        self.board=None
        self.lowprioritylist = lowprioritylist
        self.hightprioritylist = hightprioritylist
        self.criticalprioritylist = criticalprioritylist
        self.lists =None

    def connect(self):
        self.trello=TrelloApi(self.apikey,self.token)
        self.board=self.trello.boards.get(self.boardname)


    def create_card(self,name,priority,descriptions,url):

        if self.find_card(name):
            print 'Card was found ' + name
            return -1
        print 'create new card' + name
        if priority == 0:
            card= self.trello.cards.new(name,self.backlog['id'],descriptions)
        else:
            card= self.trello.cards.new(name,self.todo['id'],descriptions)
        self.trello.cards.new_attachment(card['id'],url,url)
        #self.trello.cards.new_member(card['id'],'romanvyalov1')

    def find_card(self,name):
        for i in  self.trello.boards.get_card(self.boardname):
            if i['name'] == name:
                return i
        return None

    def print_card_name(self,card):
        print card['name']

    def get_lists(self):
        for i in self.trello.boards.get_list(self.boardname):
            if i['name'] == str(self.lowprioritylist):
                self.backlog = i
            if i['name'] == str(self.hightprioritylist):
                self.todo = i
            if i['name'] == str(self.criticalprioritylist):
                self.inprogress = i
        return 0