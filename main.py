import pyautogui
from data import Email, Ticket
from selenium import webdriver

#driver = webdriver.Chrome()

Email.startNewEmail()
# driver.quit()

Email.set(Email.to)
#pyautogui.press('tab')
#Email.set(Email.cc)
