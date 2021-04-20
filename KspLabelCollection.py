from trello import Board
from KspLabel import KspLabel


class KspLabelCollection:
    def __init__(self, board: Board):
        self.__board = board
        self.__labels = []

    def __fetch_labels(self):
        to_return = []
        for t_label in self.__board.get_labels():
            to_return.append(KspLabel(t_label))
        return to_return

    def update_labels(self):
        self.__labels = self.__fetch_labels()

    def get_label_by_name(self, name: str):
        for ksp_label in self.__labels:
            if ksp_label.name == name:
                return ksp_label
        return None
