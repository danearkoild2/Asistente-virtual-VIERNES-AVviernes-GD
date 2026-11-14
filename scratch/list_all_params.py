import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('edith/edith.cdi3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== ALL PARAMETERS IN EDITH.CDI3.JSON ===")
for p in data.get('Parameters', []):
    pid = p.get('Id')
    pname = p.get('Name')
    gid = p.get('GroupId')
    # Filter dividers
    if '■' in pname or 'Divider' in pid:
        continue
    print(f"{pid:30} | {pname:25} | Group: {gid}")
