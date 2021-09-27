import pyautogui
from data import Email
import webbrowser

for x in Email.to:
    print(x)

#Email.set(Email.cc)
webbrowser.open('www.google.ca')
