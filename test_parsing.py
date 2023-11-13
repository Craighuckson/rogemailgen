import tracerwirecli
import data


def test_format_trello_ticket():
    tdata = "1234567890-1234 5th Ave,Seattle"
    assert tracerwirecli.format_trello_ticket(tdata) == ("1234567890", "1234 5TH AVE", "SEATTLE")
    tdata2 = '2023088518 FOR 71 SIR LANCELOT DR-MARKHAM'
    assert tracerwirecli.format_trello_ticket(tdata2) == ("2023088518", "71 SIR LANCELOT DR", "MARKHAM")
    tdata3 = '2023115705 FOR 7117 BATHURST ST-VAUGHAN'
    assert tracerwirecli.format_trello_ticket(tdata3) == ("2023115705", "7117 BATHURST ST", "VAUGHAN")
    assert tracerwirecli.format_trello_ticket("2023115705 67 SPRING ST, WHITCHURCH") == ("2023115705", "67 SPRING ST", "WHITCHURCH-STOUFFVILLE")
    assert tracerwirecli.format_trello_ticket("20234212061 FOR 88 STEELES AVE W-VAUGHAN") == ('20234212061', '88 STEELES AVE W', 'VAUGHAN')
    assert tracerwirecli.format_trello_ticket('2023431736-MAPLECRETE RD-VAUGHAN') == ('2023431736', 'MAPLECRETE RD', 'VAUGHAN')
    assert tracerwirecli.format_trello_ticket('Aptum - 2023411947- DON MILLS RD -TORONTO') == ('2023411947', 'DON MILLS RD', 'TORONTO')
    assert tracerwirecli.format_trello_ticket('20233710005-MULOCK DR-NEWMARKET  ENVI') == ('20233710005', 'MULOCK DR', 'NEWMARKET')

print(tracerwirecli.format_trello_ticket('20233710005-MULOCK DR-NEWMARKET  ENVI'))
