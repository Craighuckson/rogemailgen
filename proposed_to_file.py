import json
import sys

if len(sys.argv) != 6:
    print('USAGE: write_proposed.py (json_filename) ticket# address fibrename fibresize')
    sys.exit()

data = {}
data['filename'] = sys.argv[1]
data['tn'] = sys.argv[2]
data["address"] = sys.argv[3]
data["fn"] = sys.argv[4]
data['fs'] = sys.argv[5]

with open(data['filename'], "w") as jf:
    json.dump(data, jf)
