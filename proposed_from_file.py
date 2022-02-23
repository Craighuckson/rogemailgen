#proposed_from_file.py
#generates an email for proposed fibre from saved json data


from data import Email
import sys
import json

if len(sys.argv) != 2:
    print('USAGE: proposed_from_file.py json_filename')
    sys.exit()

with open(sys.argv[1]) as jf:
    data = json.load(jf)
    print(data)

tn = str(data['tn'])
add = data['address']
fn = data['fn']
fs = str(data['fs'])

print('Generating email')

Email.write_proposed(Email.tolist, Email.cclist,tn,fn,fs,add)
