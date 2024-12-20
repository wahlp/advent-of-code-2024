from itertools import product


with open('day07/input.txt') as f:
    lines = f.read().splitlines()

data: list[tuple[int, list[int]]] = []
for line in lines:
    parts = line.split(' ')
    target = int(parts[0][:-1])
    sources = [int(x) for x in parts[1:]]
    data.append((target, sources))

def check_combos(target, sources, combos) -> bool:
    for operators in combos:
        buf = sources[0]
        for o, n in zip(operators, sources[1:]):
            if o == '+':
                buf += n
            elif o == '*':
                buf *= n
            else:
                buf = int(str(buf) + str(n))
            
            if buf > target:
                break
        if buf == target:
            return True
    return False

def generate_combinations(n: int):
    return product(['+', '*', '||'], repeat=n)


total = 0
for target, sources in data:
    combos = generate_combinations(len(sources) - 1)
    is_target_achievable = check_combos(target, sources, combos)
    
    if is_target_achievable:
        total += target

print(f'{total = }')
