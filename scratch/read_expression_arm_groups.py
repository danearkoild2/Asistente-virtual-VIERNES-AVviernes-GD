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

for target in ['ParamExpression', 'ParamArmPhysics', 'ParamSleevePhysics', 'ParamSleevePendantPhysics']:
    print(f"\n=== GROUP: {target} ===")
    for pid, pname in groups.get(target, []):
        print(f"  {pid:30} : {pname}")
