import json
with open('./version.json') as f:
    j = json.load(f)

VERSION = j['version']