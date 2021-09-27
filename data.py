import pyautogui
import webbrowser

class Email:
    def set(list):
        for x in list:
            pyautogui.write(x)
            pyautogui.press(';')
        pyautogui.press('{Enter}')

    def start():
        pass
    
    to = ['tabatha.waugh@rci.rogers.com','naz.khalili@rci.rogers.com']
    cc = ['dmcgrath@cablecontrol.ca', 'b.parsons@cablecontrol.ca', 'kadisha@cablecontrol.ca','mike.falkiner@cablecontrol.ca','ray.whalen@cablecontrol.ca']


class Ticket:
	def __init__(self):
		pass
