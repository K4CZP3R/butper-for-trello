from trello import Board
from typing import List
from models.TrelloList import TrelloList
from tqdm import trange


class TrelloBoard:
    def __init__(self, _source_board: Board) -> None:
        self._this = _source_board

        self.trello_lists = self.__fetch_own_lists()
        pass

    def __fetch_own_lists(self) -> List[TrelloList]:
        _to_return = []
        for t_list in self._this.get_lists('open'):
            _to_return.append(TrelloList(t_list))
        return _to_return

    def __str__(self):
        return f"Board - {self._this.name}"

    def summary(self):
        for trello_list in self.trello_lists:
            print(f"    - List: '{trello_list._this.name}':")
            trello_list.summary()
