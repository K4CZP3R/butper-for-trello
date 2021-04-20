class ActionsCheckTime:
    def __init__(self):
        self._this = {}

    def get_action_last_check(self, action_name: str):
        if action_name not in self._this:
            return None
        return self._this[action_name]

    def set_action_last_check(self, action_name: str, val: float):
        self._this[action_name] = val
