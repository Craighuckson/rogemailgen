from data import Email, Ticket, VPN, Driver
import pyautogui as pag
import sys
import json

#tn = Ticket.get_ticket_number()
tn = input('Enter ticket number: ')

#view_ticket = pag.confirm('View ticket?', buttons=['Yes','No'])
view_ticket = input('View ticket? (y/n)')
if view_ticket.lower() == 'y':
    try:
        acct = Email.start()
    except ConnectionError:
        #pag.alert('There was an error')
        print('There was an error')
        sys.exit()
    Email.get_attachments(acct,tn)

#view_records = pag.confirm('View records?', buttons=['Yes','No'])
view_records = input('View records? (y/n)')
if view_records.lower() == 'y':
    vpn = VPN.status()
    if not vpn:
        vpn = VPN.connect()
    try:
        driver = Driver.start()
        Ticket.show_records(driver)
        
    except:
        #pag.alert('There was a problem')
        print('There was an error')
        driver.quit()
        vpn = VPN.disconnect()
        sys.exit()

#fn = Ticket.get_fibre_name()
#fs = Ticket.get_fibre_count()
#add = Ticket.get_address()
fn = input('Fibre name?')
fs = input('Fibre count?')
add= input('Address?')
vpn = VPN.disconnect()

print('Generating email')
try:
    if driver:
        driver.quit()
except NameError:
    pass
Email.write_proposed(Email.tolist, Email.cclist,tn,fn,fs,add)
