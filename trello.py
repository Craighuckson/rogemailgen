import requests
import json

TRACER_WIRE_BOARD = '5485fb41d63d87be6ce9e8c4'
TRACER_WIRE_REQUESTS = '5485fb7b43f1dd83e9b8bf8f'
PROPOSED_BOARD = '606c718031547089eb2f1f87'
NEW_PROPOSED_FIBRE = '606c730af61f347b04e26317'
INACCURATE_BOARD = '5c90ecf03021af6c1e4c6d1f'
NEW_INACCURATE_REQUESTS = '5c90ecf03021af6c1e4c6d20'
TELMAX_TRACER_REQUESTS = '652d5faf70f1bbecd6ee8447'
TRACER_REQUESTS = '652d5fc04781fc718b1cdf9e'


def _get_key():
    with open('tapikey.txt', 'r') as ak:
        apikey = ak.read()
    return apikey


def _get_token():
    with open('ttoken.txt', 'r') as at:
        token = at.read()
    return token


class Trello:
    def __init__(self):
        self.key = _get_key()
        self.token = _get_token()

    def get_cards_from_list(self, listid):
        """
        Returns a list of strings representing the 'name' field of each card
        """
        url = f"https://api.trello.com/1/lists/{listid}/cards"
        headers = {"Accept":  "application/json"}
        params = {'key':  self.key, 'token':  self.token, 'fields': 'name'}
        response = requests.request("GET", url, headers=headers, params=params)
        items = json.loads(response.text)
        return [x['name'] for x in items]

    def get_list_cards(self, listid):
        url = f"https://api.trello.com/1/lists/{listid}/cards"
        headers = {"Accept":  "application/json"}
        params = {'key':  self.key, 'token':  self.token, 'fields': 'name'}
        response = requests.request("GET", url, headers=headers, params=params)
        items = json.loads(response.text)
        return items

    def get_telmax_lists(self,board):
        url = f"https://api.trello.com/1/boards/{board}/lists"
        headers = {"Accept":  "application/json"}
        params = {'key':  self.key, 'token':  self.token, 'fields': 'name'}
        response = requests.request("GET", url, headers=headers, params=params)
        items = json.loads(response.text)
        # return name and id
        return [(x['name'],x['id']) for x in items]


    def get_card_id(self, card_name, listid):
        # Get the cards in the specified list
        cards = self.get_list_cards(listid)
            # Loop through the cards and return the ID of the card with the specified name
        for card in cards:
            if card['name'] == card_name:
                return card['id']

    def get_card_notifications(self, card_name,listid):
        # Get the ID of the card with the specified name
        card_id = self.get_card_id(card_name,listid)

        # Make a request to the Trello API to get the notifications for the specified card
        url = f"https://api.trello.com/1/cards/{card_id}/actions"
        headers = {"Accept":  "application/json"}
        params = {'key':  self.key, 'token':  self.token, 'filter': 'commentCard'}
        response = requests.request("GET", url, headers=headers, params=params)
        items = json.loads(response.text)

        # return the id and text of the comment that contains 'UNABLE TO LOCATE'

        return [(x['id'],x['data']['text']) for x in items if 'UNABLE TO LOCATE' in x['data']['text']]



if __name__ == '__main__':
    t = Trello()
    print(t.get_card_notifications('2023372955-690 LESLIE VALLEY DR, NEWMARKET', TRACER_REQUESTS))
