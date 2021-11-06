import os
import webbrowser
from exchangelib import DELEGATE, Account, Credentials
from exchangelib import Message, FileAttachment, ItemAttachment
from exchangelib.configuration import Configuration
from exchangelib.transport import NTLM

# Create account instance to get data
credentials = Credentials('craig.huckson@cablecontrol.ca','Locatesup1')
config = Configuration(server='webapp.cablecontrol.ca',auth_type=NTLM,credentials=credentials)
account = Account(primary_smtp_address='craig.huckson@cablecontrol.ca', config= config, autodiscover= False,access_type=DELEGATE)

# Get ticket number
ticketnumber = input('Enter ticket number: ')

# Search for attachments using ticket number entered and save them to \Desktop\Temp
item = account.inbox.filter(subject__contains = ticketnumber)

for attachment in item[0].attachments:
        if isinstance(attachment, FileAttachment):
            desktoptemp = os.path.join('C:\\Users\\Cr\\Desktop\\Temp', attachment.name)
            with open(desktoptemp,'wb') as f:
                f.write(attachment.content)
            print('Saved attachment to', desktoptemp)
            webbrowser.open(desktoptemp)
        elif isinstance(attachment, ItemAttachment):
            if isinstance(attachment.item, Message):
                print(attachment.item.subject, attachment.item.body)
