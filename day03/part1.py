with open('day03/input.txt') as f:
    data = f.read()

import re

r = re.findall(r'mul\((\d+),(\d+)\)', data)

total = 0
for x in r:
    total += int(x[0]) * int(x[1])

print(total)