import PySimpleGUI as sg
import webbrowser
sg.theme('Hot Dog Stand')

EMAIL = "https://webapp.cablecontrol.ca/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fwebapp.cablecontrol.ca%2fowa"
TRELLO = "https://trello.com/craighuckson/boards"
TRACER_WIRE = r"C:\Users\Cr\rogemailhelper\rogemailgen\attachments.py"
PROPOSED_FIBRE = r"C:\Users\Cr\rogemailhelper\rogemailgen\proposed_fibre.py"
INACCURATE_RECORDS = r"C:\Users\Cr\rogemailhelper\rogemailgen\inaccurate_records.py"
VPN_CONNECT = r"C:\Users\Cr\gconnect.pyw"
VPN_DISCONNECT = r"C:\Users\Cr\gdisconnect.pyw"
VPN_STATUS = r"C:\Users\Cr\vpnstat.pyw"

programs = {
	'Tracer Wire':TRACER_WIRE,
	'Proposed Fibre':PROPOSED_FIBRE,
	'Inaccurate':INACCURATE_RECORDS,
	'Connect':VPN_CONNECT,
	'Disconnect':VPN_DISCONNECT,
	'Status': VPN_STATUS,
}

layout = [
	[sg.Text('Web: '), sg.Button('Email'), sg.Button('Trello')],
	[sg.Text('Rogers email: '), sg.Button('Tracer Wire'), sg.Button('Proposed Fibre'), sg.Button('Inaccurate')],
	[sg.Text('VPN: '), sg.Button('Connect'), sg.Button('Disconnect'),sg.Button('Status')]
]

window = sg.Window('Work Scripts',layout,element_padding=(0,0),)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Exit':
		break
	for k,v in programs.items():
		if event == k:
			sg.execute_command_subprocess(v)
	if event == 'Email':
		webbrowser.open_new_tab(EMAIL)
	elif event == 'Trello':
		webbrowser.open_new_tab(TRELLO)
		
window.close()