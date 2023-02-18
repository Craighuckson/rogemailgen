import data
import sys

if len(sys.argv) != 2:
    print('Fatal error')
TICKET_NO = sys.argv[1]
acct = data.Email.start()
i = data.Email.check_for_ticket(TICKET_NO)
with open('msg.txt', 'w') as f:
    f.write(i[0].subject + "\n")
    f.write(i[0].body)
