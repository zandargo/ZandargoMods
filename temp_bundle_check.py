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
        for i,(item,count) in enumerate(zip(ci, cc)):
            print(i, item, count)
        if len(ci) > len(cc):
            for i in range(len(cc), len(ci)):
                print('extra item', i, ci[i])
        if len(cc) > len(ci):
            for i in range(len(ci), len(cc)):
                print('extra count', i, cc[i])
    else:
        print('OK')
        for i,(item,count) in enumerate(zip(ci,cc)):
            if not item or not count:
                print('empty entry', i, item, count)

print('--- invalid item names in resources bundle ---')
ref = Path('ref/items.xml').read_text('utf-8')
valid_names = set(re.findall(r'<item name="([^"]+)"', ref))
for item in items['itemAssassinStarterPackResourcesBundle']['ci']:
    if item not in valid_names:
        print('invalid resource item', item)
print('--- invalid item names in magazines bundle ---')
for item in items['itemAssassinStarterPackMagazinesBundle']['ci']:
    if item not in valid_names:
        print('invalid magazine item', item)
