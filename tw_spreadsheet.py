#creates excel file for tracer wire requests
import pyautogui

ticketnumber = pyautogui.prompt('Enter ticket number')
city = pyautogui.prompt("City/Town")
region = 'York'
fibrename = int(pyautogui.prompt('Enter fibre name'))
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
