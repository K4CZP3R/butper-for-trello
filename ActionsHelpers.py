from typing import List
from datetime import datetime

import dateutil.parser


class ActionsHelpers:
    @staticmethod
    def new_actions(actions: List[dict], last_check: float):

        new_actions = []
        new_last_check = 0
        if last_check is None:
            return [datetime.now().timestamp(), new_actions]

        for action in actions:
            action_dt = dateutil.parser.parse(action['date'])

            if action_dt.timestamp() > last_check:
                new_actions.append(action)
            new_last_check = action_dt.timestamp()
        return [new_last_check, new_actions]
