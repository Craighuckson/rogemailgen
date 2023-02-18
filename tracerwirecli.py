import sys
import os
import pyinputplus as pyip

from data import Email, Ticket, VPN
from trello import Trello, TRACER_WIRE_REQUESTS

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
    t = Trello()
    return t.get_cards_from_list(TRACER_WIRE_REQUESTS)


def format_trello_ticket(tdata: str) -> tuple:
    # checks which format trello data was put in as
    import string
    newin = ""
    index = 0
    for char in tdata:
        if char in string.ascii_uppercase:
            newin += char
        elif char in string.digits:
            newin += char
        else:
            newin += f"*{index}*"
        index += 1

    print(newin)

    try:
        tnub = int(input('Upper boundary for ticket?'))
        addlb = int(input('Lower boundary for address?'))
        addub = int(input('Upper boundary for address?'))

    except ValueError:
        return alternate_data_input()

    ticket_number = tdata[0:tnub].strip()
    address = tdata[addlb:addub].strip()
    city = tdata[addub+1:].strip()

    print(f'{ticket_number} {address} {city}')
    return ticket_number, address, city
    """
    if "," not in input:
        try:
            fields = input.split("-")
            city = fields[3].strip().capitalize().title()
            ticket_number = fields[0]
            road = fields[1].title()
            address = f"{road}, {city}"
            return ticket_number, address, city
        except IndexError:
            return alternate_data_input()

    else:
        try:
            modinput = input.replace("-", ",")
            fields = modinput.split(",")
            ticket_number = fields[0]
            city = fields[2].title().strip()
            address = fields[1].title().strip() + ", " + city
            return ticket_number, address, city

            # if there is an error here input is made manually

        except IndexError:
            return alternate_data_input()
        """

def main():

        # make sure vpn not on
        VPN.disconnect()
        trello_list = get_trello_list()
        account = Email.start()
        ticket:str = pyip.inputMenu(trello_list, prompt="Select a ticket:\n", numbered=True)

        ticket_number, address, city = format_trello_ticket(ticket)

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

def aptmain():
    """
    Main routine for Aptum email
    """

    # make sure vpn not on
    VPN.disconnect()
    trello_list = get_trello_list()
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
    choice:str = pyip.inputChoice(['rogers', 'aptum'])
    if choice == 'rogers':
        main()
    else:
        aptmain()
