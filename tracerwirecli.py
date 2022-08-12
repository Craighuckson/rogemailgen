from trello import *
from data import Email, Ticket, Driver, VPN
import pyinputplus as pyip

"""

TRACER WIRE PROCESS

-obtain list from trello

"""
def get_trello_list() -> list:
    t = Trello()
    return t.get_cards_from_list(TRACER_WIRE_REQUESTS)


def format_trello_ticket(input:str) -> tuple:
    pass


trello_list = get_trello_list()
account = Email.start()

ticket = pyip.inputMenu(trello_list,prompt='Select a ticket:',numbered=True)

ticket_number, address,city = format_trello_ticket(ticket)

viewing_attachments = pyip.inputYesNo(prompt='View ticket pictures?')

if viewing_attachments =='yes':
    images_from_contractor = Email.get_attachments(account,ticket_number)
