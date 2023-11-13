import sys
import os
import pyinputplus as pyip

from data import Email, Ticket, VPN
from trello1 import Trello, TRACER_WIRE_REQUESTS, TRACER_REQUESTS

"""

TRACER WIRE PROCESS

-obtain list from trello

"""
if len(sys.argv) > 1:
    if sys.argv[1] == 'drafts':
        Email.show_drafts(Email.start())
        sys.exit()
    else:
        print("USAGE: python tracerwirecli.py [drafts]")
        sys.exit()


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
    t: Trello = Trello()
    return t.get_card_notifications(card_name, listid)


def format_trello_ticket(s):
    unwanted_words: list[str] = [
        "Cogeco",
        "ENVI",
        "Aptum",
        "APTUM",
        "Rogers",
        "ROGERS",
        "Envi",
        "Beanfield",
        "BEANFIELD",
    ]
    for bad in unwanted_words:
        if bad in s:
            s = s.replace(bad, "")
    s = s.replace(",", " ").replace("-", " ").strip()
    print(s)
    words = s.split(" ")
    words = [word.strip() for word in words]
    print(words)
    ticket_number = words.pop(0).upper()
    print(words)
    city = words.pop(-1).upper()

    if city == "STOUFFVILLE" or city == "WHITCHURCH":
        city = "WHITCHURCH-STOUFFVILLE"
    print(words)
    address = " ".join([word.upper() for word in words if word != "FOR"]).strip()

    return ticket_number, address, city


def main():
    # make sure vpn not on
    VPN.disconnect()

    # trello_list will equal all entries in get_trello_list()
    # that dont contain "TORONTO"
    trello_list: list[str] = list(
        set([x for x in get_trello_list() if "TORONTO" not in x])
    )

    try:
        account = Email.start()
    except AttributeError:
        print("Error starting email account. Exiting...")
        sys.exit()
    ticket: str = pyip.inputMenu(
        trello_list, prompt="Select a ticket:\n", numbered=True
    )

    ticket_number, address, city = format_trello_ticket(ticket)
    address = address + "," + city
    print(f"{ticket_number} {address}")

    viewing_attachments = pyip.inputYesNo(prompt="View ticket pictures?")

    if viewing_attachments == "yes":
        Email.get_attachments(account, ticket_number)
    fibre_name: str = pyip.inputStr("Fibre name:")
    if pyip.inputYesNo("Look up fibre on Go360") == "yes":
        VPN.connect()
        Ticket.show_records(fibre_name)
    fibre_size: str = pyip.inputStr("Fibre size:")
    to_from: str = pyip.inputStr("Tracer wire needed to/from:")

    if os.path.exists(f"{fibre_name} tracer wire.png") is False:
        input("Do 360 lookup to get screenshot. Press any key when done...")

    keep_going: str = pyip.inputYesNo("Is tracer wire still needed?")

    if keep_going == "no":
        sys.exit()

    # make excel if it doesn't exist
    xl: str = f"{ticket_number} tracer wire.xlsx"
    if os.path.exists(xl) is False:
        xl = Ticket.generate_excel(
            ticket_number, address, fibre_name, fibre_size, to_from
        )

    # ensure vpn not on again
    VPN.disconnect()

    # verify that excel file and screenshot saved under proper format
    try:
        pic = f"{fibre_name} tracer wire.png"
        Email.write_tracer_wire(
            Email.tolist, Email.cclist, ticket_number, address, xl, pic
        )
        sys.exit()

    except NameError:
        fibre_name = Ticket.extract_fibre_name(f"{ticket_number} tracer wire.xlsx")
        print(fibre_name)
    except FileNotFoundError:
        input(
            __prompt="""
            Screenshot not found or saved with wrong filename.
            Ensure to save file as [fibrename] tracer wire.png.
            Ensure file present and press any key to continue..."""
        )

    if not os.path.exists(f"{fibre_name} tracer wire.png"):
        print("Screenshot not found. Exiting...")
        sys.exit()
    else:
        # save to drafts
        pic = f"{fibre_name} tracer wire.png"
        Email.write_tracer_wire(
            Email.tolist, Email.cclist, ticket_number, address, xl, pic
        )


def tmax_tracer():
    trello_list = get_telmax_list()
    ticket: str = pyip.inputMenu(
        trello_list, prompt="Select a ticket:\n", numbered=True
    )
    print(ticket)
    comment = get_comment(ticket, TRACER_REQUESTS)
    print(comment)

    # gets the locator message from list of tuples, remove backslash before @
    message = comment[0][1].replace(r"\@", "@")
    Email.write_telmax_tracer_wire(ticket, message)


def aptmain():
    """
    Main routine for Aptum email
    """

    # make sure vpn not on
    VPN.disconnect()
    # trello_list will equal all entries in get_trello_list() that do contain "TORONTO"
    trello_list = [x for x in get_trello_list() if "TORONTO" in x]

    account = Email.start()
    ticket: str = pyip.inputMenu(
        trello_list, prompt="Select a ticket:\n", numbered=True
    )

    ticket_number, address, city = format_trello_ticket(ticket)

    viewing_attachments = pyip.inputYesNo(prompt="View ticket pictures?")

    if viewing_attachments == "yes":
        Email.get_attachments(account, ticket_number)

    email_type: str = pyip.inputMenu(["tracer wire", "as builts"], numbered=True)

    if email_type == "1":
        issue: str = pyip.inputStr("Enter tracer wire issue: ")
        Email.write_aptum_tracer_wire(
            Email.bftolist, Email.cclist, ticket_number, address, issue
        )
    else:
        description: str = pyip.inputStr("Enter description for as builts needed: ")
        Email.write_aptum_asbuilts(
            Email.bftolist, Email.cclist, ticket_number, address, description
        )


if __name__ == "__main__":
    choice: str = pyip.inputMenu(["rogers", "aptum", "telmax"], numbered=True)
    if choice == "rogers":
        main()
    elif choice == "telmax":
        tmax_tracer()
    else:
        aptmain()
