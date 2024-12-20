with open('day03/input.txt') as f:
    data = f.read()

import re

muls = re.finditer(r'mul\((\d+),(\d+)\)', data)
donts = re.finditer(r"don\'t\(\)", data)
dos = re.finditer(r'do\(\)', data)

markers = []
for marker in donts:
    markers.append((marker.start(), 'dont'))
for marker in dos:
    markers.append((marker.start(), 'do'))

markers.extend([(0, 'do'), (len(data), 'do')])
markers.sort(key=lambda x: x[0])
invalid_ranges = []
for i in range(len(markers)-1):
    marker = markers[i]
    marker_next = markers[i+1]
    if marker[1] == 'dont':
        invalid_ranges.append(range(marker[0], marker_next[0]))

total = 0
for x in muls:
    if any(x.start() in ra for ra in invalid_ranges):
        continue
    total += int(x.groups()[0]) * int(x.groups()[1])

print(total)