from trello import Card


class TrelloCard:
    def __init__(self, _source_card: Card):
        self._this = _source_card

    def update_this(self, new_this: Card):
        self._this = new_this

    @property
    def id(self): return self._this.id
