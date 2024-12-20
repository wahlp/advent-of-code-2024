from collections import defaultdict


def validate(seq: list, prereqs: dict):
    for i in range(len(seq)):
        page = seq[i]
        page_prereqs = prereqs[page]
        # ensure prerequisite page already appeared
        if not all(x in seq[:i] for x in page_prereqs if x in seq):
            return False
    return True


with open('day05/input.txt') as f:
    data = f.read().splitlines()

marker = data.index('')
rules = data[:marker]
updates = data[marker + 1:]

prereqs = defaultdict(list)
for rule in rules:
    bef, aft = rule.split('|')
    prereqs[aft].append(bef)

total = 0
for update in updates:
    seq = update.split(',')
    if validate(seq, prereqs):
        mid = (len(seq) // 2)
        total += int(seq[mid])
print(total)