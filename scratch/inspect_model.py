import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('edith/edith.cdi3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

params = data.get('Parameters', [])

keywords = ['arm', 'hand', 'body', 'angle', 'breath', 'pose', 'anim', 'exp', 'oper', 'ctrl', 'shoul', 'chest', 'hip', 'z']

print(f"Total parameters: {len(params)}")
print("--- Relevant Parameters ---")
for p in params:
    pid = p.get('Id', '')
    pname = p.get('Name', '')
    gid = p.get('GroupId', '')
    if any(k in pid.lower() or k in pname.lower() or k in gid.lower() for k in keywords):
        print(f"[{gid}] {pid} -> {pname}")

# Also check edith.physics3.json
try:
    with open('edith/edith.physics3.json', 'r', encoding='utf-8') as f:
        phys = json.load(f)
    print("\n--- Physics Settings Inputs/Outputs ---")
    subgroups = phys.get('PhysicsSettings', [])
    print(f"Physics subgroups count: {len(subgroups)}")
    for sg in subgroups[:15]:
        pid_id = sg.get('Id')
        inp = [i['Source']['Id'] for i in sg.get('Input', [])]
        out = [o['Destination']['Id'] for o in sg.get('Output', [])]
        print(f"Physics Id: {pid_id} | In: {inp} -> Out: {out}")
except Exception as e:
    print(f"Physics error: {e}")
