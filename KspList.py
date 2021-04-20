from trello import Board, Label
from trello import List as TrelloList
from trello import Card as TrelloCard
from typing import List
from KspCard import KspCard
from KspRule import KspRule, KspRuleActionType, KspRuleTrigger, KspRuleAction
from KspLabel import KspLabel
from KspLabelCollection import KspLabelCollection

from ActionsCheckTime import ActionsCheckTime
import dateutil.parser
from datetime import datetime
import config
import logging


class KspList:
    def __init__(self, trello_list: TrelloList, label_collection: KspLabelCollection):
        self._this = trello_list
        self._label_collection = label_collection

        self.cards = []
        self.__fetch_cards(init_fetch=True)

        self.actions_check_times = ActionsCheckTime()

        self.log = logging.getLogger(__name__)

    @property
    def id(self): return self._this.id

    @property
    def name(self): return self._this.name

    def __fetch_cards(self, init_fetch=False):
        newly_added_cards = []
        if init_fetch:
            self.cards = []

        for l_card in self._this.list_cards():
            l_card: TrelloCard
            if not self.__card_already_present(l_card.id) or init_fetch:
                self.cards.append(KspCard(l_card, self._label_collection))
                newly_added_cards.append(self.cards[-1])
            # TODO: replace already existing cards (Maybe updated?)

        return newly_added_cards

    def __fetch_new_actions(self, action_type: str):
        new_actions = []
        actions = self._this.fetch_actions(action_type)
        actions.reverse()

        last_check = self.actions_check_times.get_action_last_check(
            action_type)
        if last_check is None:
            self.actions_check_times.set_action_last_check(
                action_type, datetime.now().timestamp())
            return []
        for action in actions:

            action_dt = dateutil.parser.parse(action['date'])

            if action_dt.timestamp() > last_check:
                new_actions.append(action)

            self.actions_check_times.set_action_last_check(
                action_type, action_dt.timestamp())
        return new_actions

    def __filter_out_actions_list(self, actions: List[dict]):
        for action in actions:
            if "listAfter" in action['data']:
                if action['data']['listAfter']['id'] != self.id:
                    actions.remove(action)

    def __card_already_present(self, card_id: str):
        for card in self.cards:
            card: KspCard
            if card.get_id() == card_id:
                return True
        return False

    def __get_card_by_id(self, card_id: str):
        for card in self.cards:
            card: KspCard
            if card.get_id() == card_id:
                return card
        return None

    def execute_rule(self, rule: KspRule):
        if rule.trigger == KspRuleTrigger.NEW_CARD:
            trello_actions = self.__fetch_new_actions('createCard')
        elif rule.trigger == KspRuleTrigger.UPDATE_CARD_MOVED_TO:
            trello_actions = self.__fetch_new_actions('updateCard')
            self.__filter_out_actions_list(trello_actions)
        else:
            print("Trigger unknown!")
            return False

        self.__fetch_cards(True)

        rets = []
        for trello_action in trello_actions:
            card_id = trello_action['data']['card']['id']
            self.log.info(f"Will execute action on card id {card_id}")
            card_in_question = self.__get_card_by_id(card_id)

            if card_in_question is None:
                self.log.warn("Card not found!")
                continue

            rets.append(card_in_question.execute_rule_actions(
                trello_action, rule.actions))
        return rets

    def __str__(self):
        return self._this.name
