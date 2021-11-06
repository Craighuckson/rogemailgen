from data import Email, Ticket, VPN, Driver
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

view_records = pag.confirm('View records?', buttons=['Yes','No'])
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

fn = Ticket.get_fibre_name()
fs = Ticket.get_fibre_count()
add = Ticket.get_address()
vpn = VPN.disconnect()
Email.write_proposed(Email.tolist, Email.cclist,tn,fn,fs,add)
