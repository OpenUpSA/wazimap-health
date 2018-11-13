import json

province = json.load(open('provinces.json'))
police = json.load(open('police_boundries.json'))
country = json.load(open('country.json'))

heath = []
i = 1
for c in country:
    c['pk'] = i
    i += 1
    heath.append(c)
for p in province:
    p['pk'] = i
    heath.append(p)
    i += 1
for b in police:
    b['pk'] = i
    heath.append(b)
    i += 1

with open('geography.json', 'w') as geo:
    json.dump(heath, geo)
