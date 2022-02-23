import requests
import json

TRACER_WIRE_BOARD = '5485fb41d63d87be6ce9e8c4'
TRACER_WIRE_REQUESTS = '5485fb7b43f1dd83e9b8bf8f'
PROPOSED_BOARD = '606c718031547089eb2f1f87'
NEW_PROPOSED_FIBRE = '606c730af61f347b04e26317'
INACCURATE_BOARD = '5c90ecf03021af6c1e4c6d1f'
NEW_INACCURATE_REQUESTS = '5c90ecf03021af6c1e4c6d20'

def _get_key():
	with open('tapikey.txt','r') as ak:
		apikey = ak.read()
		return apikey

def _get_token():
	with open('ttoken.txt','r') as at:
		token = at.read()
		return token

class Trello:
	def __init__(self):
		self.key = _get_key()
		self.token = _get_token()

	def get_cards_from_list(self,listid):
		"""
		Returns a list of strings representing the 'name' field of each card
		"""
		url = f"https://api.trello.com/1/lists/{listid}/cards"
		headers = {"Accept": "application/json"}
		params={'key': self.key,'token': self.token,'fields':'name'}
		response = requests.request("GET",url,headers=headers,params=params)
		items = json.loads(response.text)
		return [x['name'] for x in items]

t =  Trello()
print(t.get_cards_from_list(NEW_PROPOSED_FIBRE))