from trello import TrelloClient, Board, List, Card
from KspBoard import KspBoard
from KspList import KspList
from SECRETS_DONT_OPEN import key, token
from KspRule import KspRule
from time import sleep
import json
import logging
import os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

client = TrelloClient(
    api_key=key,
    api_secret=None,
    token=token,
    token_secret=None
)

board = client.get_board('607dfd07a365940a83b9f82b')

kb = KspBoard(board)
rules_json = json.load(open('rules.json', 'r'))
rules = []
for r in rules_json:
    rules.append(KspRule.from_dict(r))
kb.add_rules(rules)

while True:
    kb.watch_it_tick()
    # sleep(0.5)

# sb.cleanup()
