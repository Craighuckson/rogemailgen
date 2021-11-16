from data import Email, Ticket,VPN, Driver
import pyautogui as pag
import sys

tn = Ticket.get_ticket_number()

view_ticket = pag.confirm('View ticket?', buttons=['Yes','No'])
if view_ticket == 'Yes':
    try:
        acct = Email.start()
    except ConnectionError:
        pag.alert('There was an error')
        sys.exit()
    Email.get_attachments(acct,tn)

view_records = pag.confirm('View records?', buttons = ['Yes','No'])
if view_records == 'Yes':
    vpn = VPN.status()
if not vpn:
    vpn = VPN.connect()
try:
    driver = Driver.start()
    Ticket.show_records(driver)
except:
    pag.alert('There was a problem')
    driver.quit()
    vpn = VPN.disconnect()
    sys.exit()

img = Ticket.get_screenshot()
fn = Ticket.get_fibre_name()

vpn = VPN.disconnect()

#now make the excel spreadsheet

ticketnumber = tn
city = pag.prompt("City/Town")
region = 'York'
fibrename = fn
fibrecount = int(pag.prompt("Fibre count? "))
LSPNAME = 'CCS'
CONTACTNAME = 'Craig Huckson'
CONTACTPHONE = '(647)588-0906'
CONTACTEMAIL = 'craig.huckson@cablecontrol.ca'
description = pag.prompt('Tracer wire to/from (ie x to y)? ')
GO360_SCREENSHOT = 'Y'
new_filename = pag.prompt('Enter new filename? (must end in .xlsx) ')

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

pag.alert(f'Excel file saved as {new_filename}')

xlfile = new_filename
add = Ticket.get_address()

Email.write_tracer_wire(Email.tolist,Email.cclist, tn, add, xlfile, img)
