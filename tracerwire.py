#tracerwire.py
#fill in form automatically and send email to rogers

#todo: navigate to trello and select a page

#todo: fill in excel sheet programatically 

#get ticket info
ticketnumber = int(input("Ticket number? "))
city = input("City/Town")
region = 'York'
fibrename = input("Fibre name (from Go360)? ")
fibrecount = int(input("Fibre count? "))
LSPNAME = 'CCS'
CONTACTNAME = 'Craig Huckson'
CONTACTPHONE = '(647)588-0906'
CONTACTEMAIL = 'craig.huckson@cablecontrol.ca'
description = input('Tracer wire to/from (ie x to y)? ')
GO360_SCREENSHOT = 'Y'
new_filename = input('Enter new filename? (must end in .xlsx) ')

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

print(f'Excel file saved to C:\\Users\\Cr\\Desktop\\TEMP\\{new_filename}')

