from trello import TrelloClient
from models.TrelloBoard import TrelloBoard
from typing import List
from tqdm import trange


class TrelloSpace:
    def __init__(self, _source_client: TrelloClient) -> None:

        self._this = _source_client
        self.trello_boards = self.__fetch_own_boards()

    @classmethod
    def using_key_and_token(cls, key: str, token: str):
        return cls(TrelloClient(
            api_key=key,
            api_secret=None,
            token=token,
            token_secret=None
        ))

    def __fetch_own_boards(self) -> List[TrelloBoard]:
        _to_return = []
        _raw_boards = []
        for t_board in self._this.list_boards():
            _raw_boards.append(t_board)

        print("Processing found boards (Lists, Cards)...")
        for i in trange(len(_raw_boards)):
            _to_return.append(TrelloBoard(_raw_boards[i]))
        return _to_return

    def __str__(self):
        return f"Space - {len(self.trello_boards)} boards"

    def summary(self):
        print(f"- Space")
        for trello_board in self.trello_boards:
            print(f"  - Board: '{trello_board._this.name}':")
            trello_board.summary()

    