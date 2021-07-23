from models.TrelloSpace import TrelloSpace
from SECRETS_DONT_OPEN import key, token



ts = TrelloSpace.using_key_and_token(key, token)
ts.summary()