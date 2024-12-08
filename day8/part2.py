from collections import defaultdict
from itertools import permutations

with open('day8/sample.txt') as f:
    lines = f.read().splitlines()

signals = defaultdict(list)
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char != '.':
           signals[char].append((i, j))

def apply_offset(pos, offset):
    return (pos[0] + offset[0], pos[1] + offset[1])

def get_antinodes(n1: tuple[int, int], n2: tuple[int, int], data):
    dist = (n1[0] - n2[0], n1[1] - n2[1])
    found = []
    antinode_pos = apply_offset(n1, dist)
    while True:
        if is_oob(antinode_pos, data):
            break
        found.append(antinode_pos)
        antinode_pos = apply_offset(antinode_pos, dist)
    return found

def is_oob(pos, data):
    return not (
        0 <= pos[0] < len(data)
        and 0 <= pos[1] < len(data[0])
    )

valid_antinodes = []
for channel, members in signals.items():
    combos = permutations(members, 2)
    for n1, n2 in combos:
        antinode_pos_list = get_antinodes(n1, n2, lines)
        # if is_oob(antinode_pos, lines):
        #     continue
        for antinode_pos in antinode_pos_list:
            char_at_antinode = lines[antinode_pos[0]][antinode_pos[1]]
            if char_at_antinode != channel:
                valid_antinodes.append(antinode_pos)


# debugging
for pos in valid_antinodes:
    lines[pos[0]] = lines[pos[0]][:pos[1]] + '#' + lines[pos[0]][pos[1] + 1:]
for line in lines:
    print(line)


answer = len(set(valid_antinodes))
print(f'{answer = }')
