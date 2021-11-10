#inaccurate records

from data import Email, Ticket
import pyautogui

tn = Ticket.get_ticket_number()
add = Ticket.get_address()
report = pyautogui.prompt('Describe inaccurate records')
Email.write_inaccurate(Email.tolist, Email.cclist,tn,add,report)
