from trello import Board, Label, Card, CustomField
from trello import List as TrelloList
from KspRule import KspRuleAction, KspRuleActionType, KspRule, KspRuleTrigger
from typing import List
from ActionsHelpers import ActionsHelpers
import config
import logging
from KspLabelCollection import KspLabelCollection
from ActionsCheckTime import ActionsCheckTime
from KspLabel import KspLabel


class KspCard:
    def __init__(self, card: Card):
        self._this = card

        self._label_collection = KspLabelCollection(self._this.board)
        self.log = logging.getLogger(__name__)
        self.actions_check_times = ActionsCheckTime()

    def update_itself(self, card: Card):
        self._this = card

    def __str__(self):
        return self._this.name

    def __fetch_new_actions(self, action_type: str):
        actions = self._this.fetch_actions(action_type)
        actions.reverse()

        last_check = self.actions_check_times.get_action_last_check(
            action_type)
        ret = ActionsHelpers.new_actions(actions, last_check)
        self.actions_check_times.set_action_last_check(
            action_type, ret[0]
        )
        return ret[1]

    def execute_rule_actions_based_on_trigger(self, rule: KspRule):
        if rule.trigger == KspRuleTrigger.CHECKLIST_STATE_CHANGED:
            trello_actions = self.__fetch_new_actions(
                'updateCheckItemStateOnCard')

        rets = []
        for trello_action in trello_actions:
            rets.append(self.execute_rule_actions(trello_action, rule.actions))

        return rets

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
            elif rule_action.action_type == KspRuleActionType.CREATE_CHECKLIST:
                self.create_checklist(
                    rule_action.action_value,
                    str(rule_action.action_sub_value).split(',')
                )

                rets.append(True)
            elif rule_action.action_type == KspRuleActionType.REMOVE_CHECKLIST:
                self.remove_checklist(
                    rule_action.action_value
                )
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

    def __checklist_exists(self, checklist_name: str):
        for t_checklist in self._this.fetch_checklists():
            if t_checklist.name == checklist_name:
                return t_checklist
        return None

    def create_checklist(self, name: str, options: List[str]):
        if not self.__checklist_exists(name):
            self._this.add_checklist(name, options)

    def remove_checklist(self, name: str):
        c = self.__checklist_exists(name)
        if c is not None:
            c.delete()

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
