import tracerwirecli
import data


def test_format_trello_ticket():
    tdata = "1234567890-1234 5th Ave, Apt 2-Seattle"
    assert tracerwirecli.format_trello_ticket(tdata) == ("1234567890", "1234 5th Ave, Apt 2", "Seattle")
    tdata2 = '2023088518 FOR 71 SIR LANCELOT DR-MARKHAM'
    assert tracerwirecli.format_trello_ticket(tdata2) == ("2023088518", "71 SIR LANCELOT DR", "MARKHAM")
    tdata3 = '2023115705 FOR 7117 BATHURST ST-VAUGHAN'
    assert tracerwirecli.format_trello_ticket(tdata3) == ("2023115705", "7117 BATHURST ST", "VAUGHAN")
