from enum import Enum
from typing import Any, List
import json


class KspRuleTrigger(Enum):
    NEW_CARD = 'NEW_CARD'
    UPDATE_CARD_MOVED_TO = 'UPDATE_CARD_MOVED_TO'


class KspRuleActionType(Enum):
    ASSIGN_TO_CREATOR = 0
    ADD_COMMENT = 1
    ADD_LABEL = 2
    REMOVE_LABEL = 3
    CREATE_CUSTOM_FIELD = 4


class KspRuleAction:
    def __init__(
            self,
            action_type: KspRuleActionType,
            action_value: Any):
        self.__action_type = action_type
        self.__action_value = action_value

    @property
    def action_type(self): return self.__action_type

    @property
    def action_value(self): return self.__action_value

    def to_dict(self):
        return {
            'action_type': self.action_type.name,
            'action_value': self.action_value
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            action_type=KspRuleActionType[d['action_type']],
            action_value=d['action_value']
        )

    def __str__(self):
        return f"Do {self.action_type} with {self.action_value}"


class KspRule:
    def __init__(
            self,
            trigger: KspRuleTrigger,
            execute_in: str,
            actions: List[KspRuleAction] = []):
        self.__trigger = trigger
        self.__execute_in = execute_in

        self.__actions = actions

    def add_action(self, action: KspRuleAction):
        self.__actions.append(action)

    @property
    def actions(self): return self.__actions

    @property
    def trigger(self): return self.__trigger

    @property
    def execute_in(self): return self.__execute_in

    def to_dict(self):
        return {
            'trigger': self.trigger.name,
            'execute_in': self.execute_in,
            'actions': [a.to_dict() for a in self.actions]
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            trigger=KspRuleTrigger[d['trigger']],
            execute_in=d['execute_in'],
            actions=[KspRuleAction.from_dict(ad) for ad in d['actions']]
        )

    def __str__(self):
        return f"On '{self.trigger.name}' in '{self.execute_in}' do {len(self.actions)} actions"
