from data import Email, Ticket
import pyautogui
import subprocess

tn = pyautogui.prompt('Enter ticket number')
acct = Email.start()
Email.get_attachments(acct,tn)
#run connect.py
cd = 'C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\'

rc = subprocess.run('C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\connect.bat', cwd = cd, capture_output = True, text = True)

if rc.returncode == 0:
    pyautogui.alert('VPN connected')
else:
    pyautogui.alert('There was a problem')

pyautogui.alert('Please turn on VPN')
Ticket.show_records(fn)
img = Ticket.get_screenshot()
fn = pyautogui.prompt('Please enter fibre name')
#run disconnect.py
pyautogui.alert('Press OK to disconnect VPN')
cd = 'C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\'
dcp = subprocess.run(cd + 'disconnect.bat', capture_output = True, cwd = cd)

if dcp.returncode == 0:
    pyautogui.alert('VPN disconnected!')
else:
    pyautogui.alert('An error was present')

#now make the excel spreadsheet

ticketnumber = tn
city = pyautogui.prompt("City/Town")
region = 'York'
fibrename = fn
fibrecount = int(pyautogui.prompt("Fibre count? "))
LSPNAME = 'CCS'
CONTACTNAME = 'Craig Huckson'
CONTACTPHONE = '(647)588-0906'
CONTACTEMAIL = 'craig.huckson@cablecontrol.ca'
description = pyautogui.prompt('Tracer wire to/from (ie x to y)? ')
GO360_SCREENSHOT = 'Y'
new_filename = pyautogui.prompt('Enter new filename? (must end in .xlsx) ')

#initialize sheet
import openpyxl
wb = openpyxl.load_workbook('Tracer Wire Request Form.xlsx')
sheet = wb['Sheet1']
#insert data and save
sheet['B4'] = ticketnumber
sheet['B5'] = city + ',' + region
sheet['B6'] = fibrename
sheet['B7'] = fibrecount
sheet['D4'] = LSPNAME
sheet['D5'] = CONTACTNAME
sheet['D6'] = CONTACTPHONE
sheet['D7'] = CONTACTEMAIL
sheet['B8'] = description
sheet['B9'] = GO360_SCREENSHOT
wb.save(new_filename)

pyautogui.alert(f'Excel file saved as {new_filename}')

xlfile = new_filename
