from collections import defaultdict
from copy import deepcopy


def validate(seq: list, prereqs: dict):
    for i in range(len(seq)):
        page = seq[i]
        page_prereqs = prereqs[page]
        # ensure prerequisite page already appeared
        if not all(x in seq[:i] for x in page_prereqs if x in seq):
            return False
    return True


def fix_seq(seq: list, prereqs: dict):
    relevant = {
        page: [x for x in page_prereq if x in seq] 
        for page, page_prereq in prereqs.items() 
        if page in seq
    }

    fixed_seq = []
    for _ in seq:
        # there is only one correct solution
        # so there will only be one correct "next number"
        candidate = next(
            k for k, v in relevant.items() 
            if not v and k not in fixed_seq
        )
        for page, page_prereq in relevant.items():
            if candidate in page_prereq:
                relevant[page].remove(candidate)
        fixed_seq.append(candidate)
    return fixed_seq


with open('day5/input.txt') as f:
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
    if not validate(seq, prereqs):
        fixed_seq = fix_seq(seq, deepcopy(prereqs))
        mid = (len(fixed_seq) // 2)
        total += int(fixed_seq[mid])
print(total)