import pyautogui
from selenium import webdriver

driver = webdriver.Chrome()

class Email:
    def set(list):
        for x in list:
            pyautogui.sleep(1)
            pyautogui.write(x)
            pyautogui.press(';')
            pyautogui.sleep(0.5)

    def startNewEmail():
        driver.get('https://webapp.cablecontrol.ca/owa/#path=/mail')
        pyautogui.sleep(1)
        driver.find_element_by_id('username').click()
        driver.find_element_by_name('username').send_keys('cablecontrol\craig.huckson')
        driver.find_element_by_name('password').click()
        driver.find_element_by_name('password').send_keys('Locatesup1')
        driver.find_element_by_class_name('signinbutton').click()
        pyautogui.sleep(2)
        # click new email
        driver.find_element_by_css_selector('#\_ariaId_39').click()
        pyautogui.sleep(4)
        #this works for now
    
    to = ['tabatha.waugh@rci.rogers.com','naz.khalili@rci.rogers.com']
    cc = ['dmcgrath@cablecontrol.ca', 'b.parsons@cablecontrol.ca', 'kadisha@cablecontrol.ca','mike.falkiner@cablecontrol.ca','ray.whalen@cablecontrol.ca']


class Ticket:
    def showRecords(fibrename = ''):
        driver.get('http://10.13.218.247/go360rogersviewer/')
        driver.find_element_by_id('username').send_keys('craig.huckson')