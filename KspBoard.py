from trello import Board, Label
from KspList import KspList
from KspLabel import KspLabel
from typing import List, Optional
from KspRule import KspRule
from KspLabelCollection import KspLabelCollection
import config
import logging


class KspBoard:
    def __init__(self, board: Board):
        self._this = board

        self.rules = []
        self.log = logging.getLogger(__name__)
        self._label_collection = KspLabelCollection(self._this)
        self.lists = self.__fetch_lists()

    def __fetch_lists(self) -> List[KspList]:
        to_return = []
        for b_list in self._this.get_lists('open'):
            to_return.append(KspList(b_list, self._label_collection))
        return to_return

    def add_rules(self, rules: List[KspRule]):
        for r in rules:
            self.rules.append(r)

    def add_rules_from_json(self, rules: dict):
        for r in rules:
            print(r)
            self.rules.append(KspRule.from_dict(r))

    def watch_it_tick(self):
        for rule in self.rules:
            self.log.info(f"Executing {rule}")
            list_for_rule = self.__get_list_for_rule(rule.execute_in)

            if list_for_rule is None:
                self.log.warn(
                    f"Execute in could not be found! {rule.execute_in}")
                continue

            self.log.info(f"Will execute rule in {list_for_rule.id}")

            ret = list_for_rule.execute_rule(rule)
            self.log.info(f"Returned '{ret}'")

    def __get_list_for_rule(self, execute_in: str) -> Optional[KspList]:
        for _list in self.lists:
            if _list.name == execute_in:
                return _list
        return None

    def __str__(self):
        return self._this.name
