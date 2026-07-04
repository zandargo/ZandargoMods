from pathlib import Path
import re

path = Path('AssassinStarterPack/Config/items.xml')
text = path.read_text('utf-8')
items = {}
for match in re.finditer(r'<item name="([^"]+)">(.*?)</item>', text, re.S):
    name = match.group(1)
    body = match.group(2)
    ci = re.search(r'<property name="Create_item" value="([^"]*)"', body)
    cc = re.search(r'<property name="Create_item_count" value="([^"]*)"', body)
    items[name] = {
        'ci': ci.group(1).split(',') if ci else None,
        'cc': cc.group(1).split(',') if cc else None,
        'ci_raw': ci.group(1) if ci else None,
        'cc_raw': cc.group(1) if cc else None,
    }

ref = Path('ref/items.xml').read_text('utf-8')
valid_names = set(re.findall(r'<item name="([^"]+)"', ref))

for name in ['itemAssassinStarterPackBundle','itemAssassinStarterPackResourcesBundle','itemAssassinStarterPackMagazinesBundle']:
    print('===', name)
    info = items.get(name)
    if not info:
        print('MISSING')
        continue
    ci = info['ci']; cc = info['cc']
    print('ci len', len(ci) if ci is not None else 'none', 'cc len', len(cc) if cc is not None else 'none')
    if ci is None or cc is None:
        print('missing ci/cc')
        print(info)
        continue
    if len(ci) != len(cc):
        print('MISMATCH', len(ci), len(cc))
    else:
        print('OK')
    for i, item in enumerate(ci):
        if item not in valid_names:
            print('invalid item', name, i, item)
    for i, count in enumerate(cc):
        if not count:
            print('empty count', name, i)

