from trello import TrelloClient
from trellohelpers import Trello,TRACER_REQUESTS_ID
import pytest

def test_get_instance():
    t = Trello()
    assert isinstance(t.client,TrelloClient)

def test_get_card_warning():
    t = Trello()
    assert t.get_card_notifications('20233422961-222 BRIMSON DR, NEWMARKET',TRACER_REQUESTS_ID) == 'UNABLE TO LOCATE. DROP CONDUIT TRACE LOSES SIGNAL AT SW CORNER OF BRIMSON AND HUTCHCROFT CRT INTERSECTION'
