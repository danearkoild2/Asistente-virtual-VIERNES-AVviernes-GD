import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('edith/edith.cdi3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

groups = {}
for p in data.get('Parameters', []):
    gid = p.get('GroupId', 'NONE')
    pid = p.get('Id')
    pname = p.get('Name')
    if '■' in pname or 'Divider' in pid:
        continue
    groups.setdefault(gid, []).append((pid, pname))

# Print first 13 groups
for idx, (gid, plist) in enumerate(list(groups.items())[:13]):
    print(f"\n[{idx}] GROUP: {gid}")
    for pid, pname in plist:
        print(f"    {pid:30} : {pname}")
