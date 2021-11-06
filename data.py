from ntpath import join
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import webbrowser
import subprocess
from exchangelib import DELEGATE, Account, Credentials
from exchangelib import Message, FileAttachment, ItemAttachment
from exchangelib.configuration import Configuration
from exchangelib.transport import NTLM


'''
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
   '''
class Driver:
    def start():
        try:
            driver = webdriver.Chrome()
            return driver
        except:
            pyautogui.alert('Unable to create webdriver instance')
            return False

class Email:

    tolist = ['tabatha.waugh@rci.rogers.com','naz.khalili@rci.rogers.com']
    cclist = ['dmcgrath@cablecontrol.ca', 'b.parsons@cablecontrol.ca', 'kadisha@cablecontrol.ca','mike.falkiner@cablecontrol.ca','ray.whalen@cablecontrol.ca']

    def start():
        # Create account instance to get data
        credentials = Credentials('craig.huckson@cablecontrol.ca','Locatesup1')
        config = Configuration(server='webapp.cablecontrol.ca',auth_type=NTLM,credentials=credentials)
        account = Account(primary_smtp_address='craig.huckson@cablecontrol.ca', config= config, autodiscover= False,access_type=DELEGATE)
        return account
    
    def write_proposed(tolist,cclist,ticketnumber,fibrenumber,fibrecount,address):
        acct = Email.start()
        st = (ticketnumber,address,'proposed fibre not in field')
        substr = " - ".join(st)
        bodystr = f'''
                Tabitha / Naz:

                {fibrecount} count {fibrenumber} shows as proposed in Go360 but has not yet been installed in the field.

                Thanks,

                Craig Huckson
                '''
        m = Message(
            account=acct,
            folder=acct.drafts,
            subject=substr,
            body=bodystr,
            to_recipients = tolist,
            cc_recipients = cclist
        )
        m.save()
        pyautogui.alert('Email saved to drafts')

       
    def get_attachments(account,ticketnumber):
        # Search for attachments using ticket number entered and save them to \Desktop\Temp
        item = account.inbox.filter(subject__contains = ticketnumber)
        for attachment in item[0].attachments:
                if isinstance(attachment, FileAttachment):
                    desktoptemp = os.path.join('C:\\Users\\Cr\\Desktop\\Temp', attachment.name)
                    with open(desktoptemp,'wb') as f:
                        f.write(attachment.content)
                    print('Saved attachment to', desktoptemp)
                    #Shows images
                    webbrowser.open(desktoptemp)
                elif isinstance(attachment, ItemAttachment):
                    if isinstance(attachment.item, Message):
                        print(attachment.item.subject, attachment.item.body)


class Ticket:
    def get_ticket_number():
        # Get ticket number
        ticketnumber = pyautogui.prompt('Enter ticket number: ')
        return ticketnumber
    
    def get_fibre_name():
        # Gets fibre name
        fibre_name = pyautogui.prompt('Enter fibre name: ')
        return fibre_name

    def get_fibre_count():
        fibre_count = pyautogui.prompt('Fibre count?')
        return fibre_count
    
    def get_address():
        address = pyautogui.prompt('Address?')
        return address

    def show_records(driver,fibre_name = ''):
        #driver = webdriver.Chrome()    
        #Login to go360
        driver.get('http://10.13.218.247/go360rogersviewer/')
        driver.find_element_by_id('username').send_keys('craig.huckson')
        driver.find_element_by_id('password').send_keys('locates1')
        driver.find_element_by_xpath('/html/body/div/form/div[3]/div[2]/div/button').click()
        
        #Need a rest here sometimes or it wont work
        pyautogui.sleep(1)
        #clears previous use
        driver.find_element_by_id('form_marqueezoom_btn').click()
        driver.find_element_by_id('form_btn').click()
        pyautogui.sleep(0.5)

        '''
        if fibre_name:
            driver.find_element_by_xpath('//*[@id="tab_featureform"]/div[1]/div[3]/ul/li[2]/a').click()
            # Search by fibre name
            pyautogui.sleep(1.5)
            driver.find_element_by_xpath('//*[@id="assetName"]/option[4]').click()
            pyautogui.sleep(1.5)
            driver.find_element_by_id('assetsearchtitlesid1').send_keys('c')
            pyautogui.sleep(1.5)
            driver.find_element_by_id('assetsearchtextid1').send_keys(fibre_name)
            driver.find_element_by_id('assetssearchbutton').click()

        else:
            # search by intersection
            driver.find_element_by_xpath('//*[@id="tab_featureform"]/div[1]/div[3]/ul/li[1]/a/span[1]').click()
            driver.find_element_by_id('intersectionSearchInput1').send_keys(street)
            driver.find_element_by_id('intersectionSearchInput2').send_keys(intersection)
            driver.find_element_by_css_selector('#id_search_div > div:nth-child(1) > table > tbody > tr:nth-child(6) > td:nth-child(4) > a').click()

        '''
    def get_screenshot():
        win = pyautogui.getWindowsWithTitle('Go360')[0]
        win.activate()
        pyautogui.alert('Press OK to take screenshot and close Go360')
        pyautogui.sleep(2)
        pyautogui.screenshot('image.png',region=(15,50,1338,665))
        pyautogui.alert('Screenshot saved')
        pyautogui.sleep(1)

class VPN:
    def status(vpn=''):
        if not vpn:
            return False
        else:
            return True


    def connect():
        cd = 'C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\'
        rc = subprocess.run('C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\connect.bat', cwd = cd, capture_output = True, text = True)
        if rc.returncode == 0:
            pyautogui.alert('VPN connected')
        else:
            pyautogui.alert('There was a problem')
        return True

    def disconnect():
        cd = 'C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\'
        dcp = subprocess.run(cd + 'disconnect.bat', capture_output = True, cwd = cd)
        if dcp.returncode == 0:
            pyautogui.alert('VPN disconnected!')
        else:
            pyautogui.alert('An error was present')
        return False


