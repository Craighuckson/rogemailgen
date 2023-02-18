import sys
from data import Email

if len(sys.argv) != 2:
    print('Usage: tkcheck.py <ticket number>')
    sys.exit()

Email.check_for_ticket(sys.argv[1])
