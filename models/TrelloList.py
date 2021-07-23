from trello import List as List
from typing import List as typing_list
from models.TrelloCard import TrelloCard


class TrelloList:
    def __init__(self, _source_list: List):
        self._this = _source_list
        self.trello_cards: List[TrelloCard] = []
        self.__fetch_own_cards(True)

    def __fetch_own_cards(self, init_fetch=False) -> typing_list[TrelloCard]:
        fetched_now = []

        if init_fetch:
            self.trello_cards = []
        for t_card in self._this.list_cards():
            card_ret = self.__card_already_exists(t_card)
            if card_ret == -1:
                self.trello_cards.append(TrelloCard(t_card))
                fetched_now.append(self.trello_cards[-1])
            else:
                self.trello_cards[card_ret].update_this(t_card)

        return fetched_now

    def __card_already_exists(self, trello_card: TrelloCard) -> int:
        for card in self.trello_cards:
            card: TrelloCard
            if card.id == trello_card.id:
                return self.trello_cards.index(card)
        return -1

    def summary(self):
        for trello_card in self.trello_cards:
            print(f"      - Card: '{trello_card._this.name}':")
            
