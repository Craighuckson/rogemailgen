
from tracerwirecli import format_trello_ticket

def test_for_removed_from_ticket_name():
    assert format_trello_ticket('20234214557-FOR 7 ALAN FRANCIS LANE-MARKHAM') == ('20234214557', '7 ALAN FRANCIS LANE', 'MARKHAM')
