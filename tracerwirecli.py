import sys
import os
import pyinputplus as pyip

from data import Email, Ticket, VPN
from trello import Trello, TRACER_WIRE_REQUESTS, TRACER_REQUESTS

"""

TRACER WIRE PROCESS

-obtain list from trello

"""


def alternate_data_input() -> tuple:
    print("Wrong input format. Switching to manual input")
    ticket_number = input("Ticket number:")
    address = input("Address:")
    city = input("City:")
    return ticket_number, address, city


def get_trello_list() -> list:
    # get list of tickets from trello
    t = Trello()
    return t.get_cards_from_list(TRACER_WIRE_REQUESTS)

def get_telmax_list() -> list:
    t = Trello()
    return t.get_cards_from_list(TRACER_REQUESTS)

def get_comment(card_name, listid):
    t = Trello()
    return t.get_card_notifications(card_name,listid)


def format_trello_ticket(tdata: str) -> tuple:
    # formats the ticket data string received from trello and returns a tuple (ticket number, address, city)
    #parse the ticket number, first character to last digit of first word. use regex
    import re
    ticket_number = re.search(r'\d+', tdata).group()

    #parse the address, either first character after first "-" to last character before next "-" or start of first word after "FOR" to last character before next "-"
    address = tdata[tdata.find("-")+1:tdata.rfind("-")].strip()
    if address == "":
        address = tdata[tdata.find("FOR")+3:tdata.rfind("-")].strip()

    #parse the city, first character after last "-" to end of string
    city = tdata[tdata.rfind("-")+1:]

    return ticket_number, address, city

def main():

        # make sure vpn not on
        VPN.disconnect()

        #trello_list will equal all entries in get_trello_list() that dont contain "TORONTO"
        trello_list =list(set([x for x in get_trello_list() if "TORONTO" not in x]))

        account = Email.start()
        ticket:str = pyip.inputMenu(trello_list, prompt="Select a ticket:\n", numbered=True)

        ticket_number, address, city = format_trello_ticket(ticket)
        address = address + ',' + city
        print(f'{ticket_number} {address}')

        viewing_attachments = pyip.inputYesNo(prompt="View ticket pictures?")

        if viewing_attachments == "yes":
            images_from_contractor = Email.get_attachments(account, ticket_number)
        fibre_name: str = pyip.inputStr("Fibre name:")
        if pyip.inputYesNo("Look up fibre on Go360") == 'yes':
            VPN.connect()
            Ticket.show_records(fibre_name)
        fibre_size: str = pyip.inputStr("Fibre size:")
        to_from: str = pyip.inputStr("Tracer wire needed to/from:")

        if os.path.exists(f'{fibre_name} tracer wire.png') == False:
            input('Do 360 lookup to get screenshot. Press any key when done...')

        keep_going:str = pyip.inputYesNo("Is tracer wire still needed?")

        if keep_going == "no":
            sys.exit()

        # make excel if it doesn't exist
        xl:str = f'{ticket_number} tracer wire.xlsx'
        if os.path.exists(xl) == False:
            xl = Ticket.generate_excel(ticket_number, address, fibre_name, fibre_size, to_from)

        #ensure vpn not on again
        VPN.disconnect()

        # verify that excel file and screenshot saved under proper format
        try:
            pic = f'{fibre_name} tracer wire.png'
            Email.write_tracer_wire(Email.tolist,Email.cclist
            ,ticket_number,address,xl,pic)
            sys.exit()

        except NameError:
            fibre_name  = Ticket.extract_fibre_name(f'{ticket_number} tracer wire.xlsx')
            print(fibre_name)
        except FileNotFoundError:
            input('Screenshot not found or saved with wrong filename. Ensure to save file as [fibrename] tracer wire.png. Ensure file present and press any key to continue...')

        if not os.path.exists(f'{fibre_name} tracer wire.png'):
            print('Screenshot not found. Exiting...')
            sys.exit()
        else:
        #save to drafts
            pic = f'{fibre_name} tracer wire.png'
            Email.write_tracer_wire(Email.tolist,Email.cclist
            ,ticket_number,address,xl,pic)


def tmax_tracer():
    trello_list = get_telmax_list()
    account = Email.start()
    ticket:str = pyip.inputMenu(trello_list, prompt="Select a ticket:\n", numbered=True)
    print(ticket)
    print(get_comment(ticket,TRACER_REQUESTS))
    message = pyip.inputStr("Enter message: ")
    Email.write_telmax_tracer_wire(ticket, message)

def aptmain():
    """
    Main routine for Aptum email
    """

    # make sure vpn not on
    VPN.disconnect()
    #trello_list will equal all entries in get_trello_list() that do contain "TORONTO"
    trello_list = [x for x in get_trello_list() if "TORONTO" in x]

    account = Email.start()
    ticket:str = pyip.inputMenu(trello_list, prompt="Select a ticket:\n", numbered=True)

    ticket_number, address, city = format_trello_ticket(ticket)

    viewing_attachments = pyip.inputYesNo(prompt="View ticket pictures?")

    if viewing_attachments == "yes":
        Email.get_attachments(account, ticket_number)

    email_type: str = pyip.inputMenu(['tracer wire', 'as builts'],numbered=True)

    if email_type == "1":
        issue:str = pyip.inputStr("Enter tracer wire issue: ")
        Email.write_aptum_tracer_wire(Email.bftolist, Email.cclist, ticket_number, address,issue)
    else:
        description:str = pyip.inputStr("Enter description for as builts needed: ")
        Email.write_aptum_asbuilts(Email.bftolist, Email.cclist, ticket_number, address, description)


if __name__ == '__main__':
    choice:str = pyip.inputChoice(['rogers', 'aptum', 'telmax'])
    if choice == 'rogers':
        main()
    elif choice == 'telmax':
        tmax_tracer()
    else:
        aptmain()
