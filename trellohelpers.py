from trello import TrelloClient

TRACER_WIRE_BOARD_ID = '5485fb41d63d87be6ce9e8c4'
TRACER_WIRE_REQUESTS_ID = '5485fb7b43f1dd83e9b8bf8f'
PROPOSED_BOARD_ID = '606c718031547089eb2f1f87'
NEW_PROPOSED_FIBRE_ID = '606c730af61f347b04e26317'
INACCURATE_BOARD_ID = '5c90ecf03021af6c1e4c6d1f'
NEW_INACCURATE_REQUESTS_ID = '5c90ecf03021af6c1e4c6d20'
TELMAX_TRACER_REQUESTS_ID = '652d5faf70f1bbecd6ee8447'
TRACER_REQUESTS_ID = '652d5fc04781fc718b1cdf9e'

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
        self.client = TrelloClient(_get_key(), _get_token())

    def get_cards_from_list(self, listid):
        """
        Returns a list of strings representing the 'name' field of each card
        """
        return [x.name for x in self.client.get_list(listid).list_cards()]

    def get_list_cards(self, listid):
        return self.client.get_list(listid).list_cards()

    def get_lists_from_board(self,boardid):
        return [(x.name,x.id) for x in self.client.get_board(boardid).all_lists()]

    def get_card_id(self, card_name, listid):
        cards = self.client.get_list(listid).list_cards()
        for card in cards:
            if card.name == card_name:
                return card.id
        return None

    def get_card_notifications(self, card_name, listid):
        cardid = self.get_card_id(card_name, listid)
        card = self.client.get_card(cardid)
        comments = card.comments
        print(comments)
        return next((remark['data']['text'] for remark in comments if 'UNABLE TO LOCATE' in remark['data']['text']),"")


if __name__ == '__main__':
    t = Trello()
    print(t.get_cards_from_list(TRACER_WIRE_REQUESTS_ID))
