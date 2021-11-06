import pyautogui
win = pyautogui.getWindowsWithTitle('Go360')[0]
win.activate()
pyautogui.alert('Press OK to take screenshot and close Go360')
pyautogui.sleep(2)
pyautogui.screenshot('image.png',region=(15,50,1338,665))
pyautogui.alert('Screenshot saved')
pyautogui.sleep(1)
