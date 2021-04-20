from trello import Label


class KspLabel:
    def __init__(self, trello_label: Label):
        self.__this = trello_label

    @property
    def name(self): return self.__this.name

    @property
    def id(self): return self.__this.id

    @property
    def org(self): return self.__this
