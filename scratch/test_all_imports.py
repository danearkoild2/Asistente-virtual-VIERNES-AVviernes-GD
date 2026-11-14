import os
import sys
import importlib

sys.path.insert(0, os.path.abspath('.'))

folders = ['actions', 'core', 'plugins', 'security', 'system_monitor', 'memory', 'integrations']
results = {'ok': 0, 'failed': []}

for folder in folders:
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith('.py') and not f.startswith('__'):
                rel = os.path.relpath(os.path.join(root, f), '.')
                mod_name = rel.replace('\\', '/').replace('/', '.').removesuffix('.py')
                try:
                    importlib.import_module(mod_name)
                    results['ok'] += 1
                except Exception as e:
                    results['failed'].append((mod_name, f"{type(e).__name__}: {e}"))

print(f"Total importados OK: {results['ok']}")
print(f"Total fallidos: {len(results['failed'])}")
for mod, err in results['failed']:
    print(f"FAIL: {mod} -> {err}")
