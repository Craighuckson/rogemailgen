# rogworkgui.py
import base64
from trello import *
from data import Email, Ticket, Driver
import PySimpleGUI as sg
import io
import PIL.Image
import logging

sg.theme("black")

#log to dump stack trace on failure
logging.basicConfig(filename='rguilog.txt', level=logging.INFO,
format=' %(asctime)s -  %(levelname)s -  %(message)s')

# functions#


def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize(
            (int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS
        )
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def format_input_string(input):
    """
    Returns ticket number, address, city from Trello input string
    """
    try:
        fields = input.split("-")
        city = fields[3].strip().capitalize().title()
        ticket = fields[0]
        road = fields[1].title()
        address = f"{road}, {city}"
        return ticket, address, city
    except IndexError:
        sg.popup("Improper input!")


t = Trello()
trellotw = [""]
trelloprop = [""]
trelloir = [""]

tab_tracerwire_layout = [
    [
        sg.Combo(trellotw, k="twlist", enable_events=True),
        sg.Button("Update list", k="twupdate"),
    ],
    [sg.T("Fibre name: "), sg.Input(k="fn_tw", do_not_clear=False)],
    [sg.Text("Fibre size: "), sg.Input(k="fs_tw", do_not_clear=False)],
    [sg.Text("To and From"), sg.Input(k="tofrom")],
    [sg.Text("Screenshot"), sg.I(k="pic"), sg.FileBrowse()],
    [sg.Text("Excel file: "), sg.I(k="xl"), sg.FileBrowse()],
    [
        sg.Button("Generate Email", k="email_tw"),
        sg.Button("Make Excel File", k="makexl"),
    ],
]

tab_proposed_layout = [
    [
        sg.Combo(trelloprop, k="tplist", expand_x=True, enable_events=True),
        sg.Button("Update list", k="propupdate", enable_events=True),
    ],
    [sg.Text("Fibre name: "), sg.Input(k="fn_prop")],
    [sg.T("Fiber size: "), sg.I(k="fs_prop")],
    [sg.Button("Generate email", k="email_prop")],
]

tab_inaccurate_layout = [
    [
        sg.Combo(trelloir, k="tilist", enable_events=True),
        sg.Button("Update list", k="irupdate", enable_events=True),
    ],
    [sg.Text("Describe issue: "), sg.Multiline(k="description")],
    [sg.Button("Generate email", k="email_inaccurate")],
]

lcol = [
    # [sg.Titlebar(title='Email Helper')],
    [
        sg.Text("Input string"),
        sg.Input(k="inputstr", do_not_clear=False),
        sg.Button(button_text="Format", k="formatstr"),
    ],
    [sg.Text("Ticket Number: "), sg.Input(k="tn")],
    [sg.Text("Address: "), sg.Input(k="address")],
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Tracer Wire", tab_tracerwire_layout),
                    sg.Tab("Proposed", tab_proposed_layout),
                    sg.Tab("Inaccurate", tab_inaccurate_layout),
                ]
            ]
        )
    ],
    [
        sg.Button("Get attachments", k="get_attachments"),
        sg.Button("View Records", k="view_records"),
    ],
]
rcol = [
    [sg.Listbox(values=[], k="attachment_list",auto_size_text=True,expand_y=True, enable_events=True)],
    [sg.Image(k='viewer',expand_x=True,expand_y=True)],
]

layout = [
    [
        sg.Column(lcol,pad=5, vertical_alignment='top'),
        sg.Column(rcol, scrollable=True,expand_x=True,expand_y=True),
    ]
]

window = sg.Window("Email Helper", layout, finalize=True,resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "twupdate":
        window["twlist"].update(values=t.get_cards_from_list(TRACER_WIRE_REQUESTS))
        window["twlist"].expand(expand_x=True)
    if event == "twlist":
        window["inputstr"].update(values["twlist"])
    if event == "propupdate":
        window["tplist"].update(values=t.get_cards_from_list(NEW_PROPOSED_FIBRE))
        window["tplist"].expand(expand_x=True)
    if event == "tplist":
        window["inputstr"].update(values["tplist"])
    if event == "irupdate":
        window["tilist"].update(values=t.get_cards_from_list(NEW_INACCURATE_REQUESTS))
        window["tilist"].expand(expand_x=True)
    if event == "tilist":
        window["inputstr"].update(values["tilist"])
    if event == "formatstr":
        try:
            vals = format_input_string(values["inputstr"])
            window["tn"].update(vals[0])
            window["address"].update(vals[1])
        except TypeError:
            pass
    if event == "email_tw":
        Email.write_tracer_wire(
            Email.tolist,
            Email.cclist,
            values["tn"],
            values["address"],
            values["xl"],
            values["pic"],
        )
    if event == "email_prop":
        Email.write_proposed(
            Email.tolist,
            Email.cclist,
            values["tn"],
            values["fn_prop"],
            values["fs_prop"],
            values["address"],
        )
    if event == "email_inaccurate":
        Email.write_inaccurate(
            Email.tolist,
            Email.cclist,
            values["tn"],
            values["address"],
            values["description"],
        )
    if event == "makexl":
        Ticket.generate_excel(
            values["tn"],
            values["address"],
            values["fn_tw"],
            values["fs_tw"],
            values["tofrom"],
        )
    if event == "get_attachments":
        acct = Email.start()
        window.perform_long_operation((lambda: Email.get_attachments(acct,values['tn'])), '-FUNCTION COMPLETED-')
        window['attachment_list'].update(['Waiting on attachments...'])
    if event == '-FUNCTION COMPLETED-':
        if values['-FUNCTION COMPLETED-']:
            file_list = values['-FUNCTION COMPLETED-']
            fnames = [x for x in file_list]
            window['attachment_list'].update(fnames)
        else:
            window['attachment_list'].update(["Couldn't obtain attachments"])
    if event == 'attachment_list':
        try:
            window['viewer'].update(data=convert_to_bytes(values['attachment_list'][0]))
        except IndexError:
            sg.popup("The files for " + str(values['tn']) + " could not be obtained")
        except FileNotFoundError:
             sg.popup("The files for " + str(values['tn']) + " could not be obtained")
    if event == "view_records":
        sg.popup("Ensure VPN is connected and hit OK to continue")
        d = Driver.start()
        Ticket.show_records(d)
