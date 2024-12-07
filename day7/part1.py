with open('day7/input.txt') as f:
    lines = f.read().splitlines()

data: list[tuple[int, list[int]]] = []
for line in lines:
    parts = line.split(' ')
    target = int(parts[0][:-1])
    sources = [int(x) for x in parts[1:]]
    data.append((target, sources))

def evaluate_expr(sources, operators) -> int:
    buf = sources[0]
    for o, n in zip(operators, sources[1:]):
        if o == '+':
            buf += n
        else:
            buf *= n
    return buf

from itertools import product

def generate_combinations(n: int):
    return product(['+', '*'], repeat=n)


total = 0
for target, sources in data:
    is_target_achievable = False
    combos = generate_combinations(len(sources) - 1)
    for operators in combos:
        s = ' '.join(' '.join(str(x) for x in t) for t in zip(sources, operators)) + ' ' + str(sources[-1])
        outcome = evaluate_expr(sources, operators)
        # print(f'{target}: {outcome} = {s}')
        if outcome == target:
            # print('achievable')
            is_target_achievable = True
            break
    
    if is_target_achievable:
        total += target

print(f'{total = }')
