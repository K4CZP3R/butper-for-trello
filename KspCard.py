from trello import Board, Label, Card
from trello import List as TrelloList
from KspRule import KspRuleAction, KspRuleActionType
from typing import List
import config
import logging
from KspLabelCollection import KspLabelCollection
from KspLabel import KspLabel


class KspCard:
    def __init__(self, card: Card, label_collection: KspLabelCollection):
        self._this = card

        self._label_collection = label_collection
        self.log = logging.getLogger(__name__)

    def __str__(self):
        return self._this.name

    def execute_rule_actions(self, trello_action: dict, rule_actions: List[KspRuleAction]):
        rets = []
        for rule_action in rule_actions:
            self.log.info(f"Executing action: {rule_action}")
            if rule_action.action_type == KspRuleActionType.ADD_COMMENT:
                self.add_comment(rule_action.action_value)
                rets.append(True)
            elif rule_action.action_type == KspRuleActionType.ADD_LABEL \
                    or rule_action.action_type == KspRuleActionType.REMOVE_LABEL:

                self._label_collection.update_labels()
                label_in_question = self._label_collection.get_label_by_name(
                    rule_action.action_value)
                if not label_in_question:
                    rets.append(False)
                    continue

                if rule_action.action_type == KspRuleActionType.ADD_LABEL and not self.__label_exists(label_in_question.id):
                    self.add_label(label_in_question)
                elif rule_action.action_type == KspRuleActionType.REMOVE_LABEL and self.__label_exists(label_in_question.id):
                    self.remove_label(label_in_question)
                rets.append(True)

            elif rule_action.action_type == KspRuleActionType.ASSIGN_TO_CREATOR:
                self.assign_to(
                    trello_action['idMemberCreator']
                )
                rets.append(True)
            elif rule_action.action_type == KspRuleActionType.CREATE_CUSTOM_FIELD:
                self.create_custom_field(rule_action.action_value)
                rets.append(True)
            else:
                print(f"Unknown action type!")
                rets.append(False)
        return rets

    def __label_exists(self, label_id: str):
        if self._this.labels is None:
            return False
        for trello_label in self._this.labels:
            trello_label: Label
            if trello_label.id == label_id:
                return True
        return False

    def create_custom_field(self, field: str):
        self._this.board: Board
        self._this.board.add_custom_field_definition(field, 'checkbox')

    def add_label(self, label: KspLabel):
        self._this.add_label(label.org)

    def remove_label(self, label: KspLabel):
        self._this.remove_label(label.org)

    def add_comment(self, val: str):
        self._this.comment(val)

    def assign_to(self, member_id: str):
        self._this.assign(member_id)

    def get_id(self):
        return self._this.id
