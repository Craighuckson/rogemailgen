import PySimpleGUI as sg

sg.theme("black")

from ntpath import join
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import webbrowser
import subprocess
from exchangelib import DELEGATE, Account, Credentials
from exchangelib import Message, FileAttachment, ItemAttachment
from exchangelib.configuration import Configuration
from exchangelib.transport import NTLM
import openpyxl
from isvpn import is_vpn
import pprint
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


class Driver:
    def start():
        try:
            return webdriver.Chrome()
        except:
            pyautogui.alert("Unable to create webdriver instance")
            return False


class Email:

    bftolist = ["emanuel@beanfield.com"]
    tolist = ["tabatha.waugh@rci.rogers.com", "Hissam.ElSayed@rci.rogers.com"]
    cclist = [
        "dmcgrath@cablecontrol.ca",
        "b.parsons@cablecontrol.ca",
        "kadisha@cablecontrol.ca",
        "tony.knibbe@cablecontrol.ca",
        "ray.whalen@cablecontrol.ca",
    ]

    def start() -> Account:
        # Create account instance to get data
        try:
            credentials = Credentials("craig.huckson@cablecontrol.ca", "Locatesup1")
            config = Configuration(
                server="webapp.cablecontrol.ca", auth_type=NTLM, credentials=credentials
            )
            account = Account(
                primary_smtp_address="craig.huckson@cablecontrol.ca",
                config=config,
                autodiscover=False,
                access_type=DELEGATE,
            )
            return account
        except AttributeError:
            sg.popup("Couldn't access email account")
            return None

    def check_for_ticket(ticket_no) -> None:
        acct = Email.start()
        item = acct.inbox.filter(subject__contains=ticket_no)
        return item
        '''
        for _ in item:
            print(_.subject)
            print(_.datetime_received)
            print(_.body)
            '''

    def write_proposed(
        tolist, cclist, ticketnumber, fibrenumber, fibrecount, address
    ) -> None:
        acct = Email.start()
        st = (ticketnumber, address, "proposed fibre not in field")
        substr = " - ".join(st)
        bodystr = f"""
Hello,

{fibrecount} count {fibrenumber} shows as proposed in Go360 but was not installed in the field at the time of the locate.

Thanks,

Craig Huckson
                """
        m = Message(
            account=acct,
            folder=acct.drafts,
            subject=substr,
            body=bodystr,
            to_recipients=tolist,
            cc_recipients=cclist,
        )
        m.save()
        sg.popup("Email saved to drafts")

    def write_inaccurate(tolist, cclist, ticketnumber, address, report):
        acct = Email.start()
        st = (ticketnumber, address, "inaccurate records")
        substr = " - ".join(st)
        bodystr = f"""
Hello,

{report}

Thanks,

Craig Huckson
                """
        m = Message(
            account=acct,
            folder=acct.drafts,
            subject=substr,
            body=bodystr,
            to_recipients=tolist,
            cc_recipients=cclist,
        )
        m.save()
        sg.popup("Email saved to drafts")

    def write_tracer_wire(tolist, cclist, ticketnumber, address, xl, pic):
        acct = Email.start()
        st = (ticketnumber, address, "tracer wire needed")
        substr = " - ".join(st)
        bodystr = f"""
Hello,

Please see the attached

Thanks,

Craig Huckson
                """
        m = Message(
            account=acct,
            folder=acct.drafts,
            subject=substr,
            body=bodystr,
            to_recipients=tolist,
            cc_recipients=cclist,
        )
        with open(xl, mode="rb") as spreadsheet:
            xlfile = FileAttachment(
                name=os.path.basename(xl), content=spreadsheet.read()
            )
        with open(pic, mode="rb") as img:
            picture = FileAttachment(name=os.path.basename(pic), content=img.read())
        m.attach(xlfile)
        m.attach(picture)
        m.save()
        sg.popup("Email saved to drafts")

    def get_attachments(account, ticketnumber):
        # Search for attachments using ticket number entered and save them to \Desktop\Temp
        # returns a file list
        try:
            file_list = []
            item = account.inbox.filter(subject__contains=ticketnumber)
            for attachment in item[0].attachments:
                if isinstance(attachment, FileAttachment):
                    temp = os.path.join(".\\temp", attachment.name)
                    with open(temp, "wb") as f:
                        f.write(attachment.content)
                    file_list.append(temp)
                    print("Saved attachment to", temp)
                    # Shows images
                    webbrowser.open(temp)
                elif isinstance(attachment, ItemAttachment):
                    if isinstance(attachment.item, Message):
                        print(attachment.item.subject, attachment.item.body)
        except IndexError:
            pass
        return file_list

    def write_aptum_tracer_wire(bftolist, cclist, ticketnumber, address, issue):
        acct = Email.start()
        subject_line: str = " - ".join([ticketnumber, address, "Tracer Wire Needed"])
        bodystr: str = f"""
Hello,

We require a tracer wire for {issue}

Thanks,

Craig Huckson
"""
        m: Message = Message(
            account=acct,
            folder=acct.drafts,
            subject=subject_line,
            body=bodystr,
            to_recipients=bftolist,
            cc_recipients=cclist,
        )
        m.save()
        sg.popup("Saved to drafts")

    def write_aptum_asbuilts(bftolist, cclist, ticketnumber, address, description):
        acct: Account = Email.start()
        subject_line: str = " - ".join([ticketnumber, address, "As-Builts Needed"])
        bodystr: str = f"""
Hello,

We require as-builts for {description}.

Thanks,

Craig Huckson
"""
        m: Message = Message(
            account=acct,
            folder=acct.drafts,
            subject=subject_line,
            body=bodystr,
            to_recipients=bftolist,
            cc_recipients=cclist,
        )
        m.save()
        sg.popup("Message saved to drafts")


class Ticket:
    def get_ticket_number() -> str:
        # Get ticket number
        ticketnumber: str = pyautogui.prompt("Enter ticket number: ")
        return ticketnumber

    def get_fibre_name():
        # Gets fibre name
        fibre_name = pyautogui.prompt("Enter fibre name: ")
        return fibre_name

    def get_fibre_count():
        fibre_count = pyautogui.prompt("Fibre count?")
        return fibre_count

    def get_address():
        address = pyautogui.prompt("Address?")
        return address

    def show_records(fibre_name=""):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = Driver.start()
        driver.get("http://10.13.218.247/go360rogersviewer/")
        driver.find_element_by_id("username").send_keys("craig.huckson")
        driver.find_element_by_id("password").send_keys("locates1")
        driver.find_element_by_xpath(
            "/html/body/div/form/div[3]/div[2]/div/button"
        ).click()

        # Need a rest here sometimes or it wont work
        pyautogui.sleep(1)
        # clears previous use
        driver.find_element_by_id("form_marqueezoom_btn").click()
        driver.find_element_by_id("form_btn").click()
        pyautogui.sleep(0.5)

        driver.find_element_by_xpath('//*[@id="tab_featureform"]/div[1]/div[3]/ul/li[2]/a').click()
        # Search by fibre name
        #pyautogui.sleep(1.5)
        ddelement = Select(driver.find_element_by_xpath('//*[@id="assetName"]'))
        ddelement.select_by_visible_text('Fiber Cables - themed by Risk')
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="assetsearchtitlesid1"]')))
        ddelement2 = Select(driver.find_element_by_xpath('//*[@id="assetsearchtitlesid1"]'))
        ddelement2.select_by_visible_text('Cable Name')
        pyautogui.sleep(1.5)
        driver.find_element_by_id('assetsearchtextid1').send_keys(fibre_name)
        driver.find_element_by_id('assetssearchbutton').click()


    def get_screenshot() -> str:
        win = pyautogui.getWindowsWithTitle("Go360")[0]
        win.activate()
        im = pyautogui.prompt("Enter image name")
        pyautogui.sleep(2)
        pyautogui.screenshot(im + ".png", region=(15, 50, 1338, 665))
        pyautogui.alert("Screenshot saved")
        pyautogui.sleep(1)
        im = im + ".png"
        return im

    def generate_excel(tn, address, fn, fs, tofrom) -> str:
        new_filename = tn + " tracer wire.xlsx"
        LSPNAME = "CCS"
        CONTACTNAME = "Craig Huckson"
        CONTACTPHONE = "(647)588-0906"
        CONTACTEMAIL = "craig.huckson@cablecontrol.ca"
        REGION = "York"
        GO360_SCREENSHOT = "Y"
        wb = openpyxl.load_workbook("Tracer Wire Request Form.xlsx")
        print(str(wb))
        sheet = wb["Sheet1"]
        sheet["B4"] = tn
        sheet["B5"] = address + ", " + REGION
        sheet["B6"] = fn
        sheet["B7"] = fs
        sheet["D4"] = LSPNAME
        sheet["D5"] = CONTACTNAME
        sheet["D6"] = CONTACTPHONE
        sheet["D7"] = CONTACTEMAIL
        sheet["B8"] = tofrom
        sheet["B9"] = GO360_SCREENSHOT
        wb.save(new_filename)
        print(f"Excel file saved as {new_filename}")
        return new_filename

    def extract_fibre_name(xlfile) -> str:
        f = openpyxl.load_workbook(xlfile)
        sheet = f["Sheet1"]
        return sheet["B6"].value


class VPN:
    def status(vpn=""):
        if not vpn:
            return False
        else:
            return True

    def vpn_toggle():
        subprocess.run("C:\\Program Files\\AutoHotkey\\AutoHotkeyU64.exe vpnpy.ahk")

    def check_status():
        return is_vpn()

    def connect():
        if VPN.check_status():
            pass
        else:
            VPN.vpn_toggle()

    def disconnect():
        if VPN.check_status():
            VPN.vpn_toggle()

if __name__ == "__main__":
    Ticket.show_records("10151953")
