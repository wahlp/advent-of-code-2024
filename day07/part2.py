def parse_input(filename):
    with open(f'day07/{filename}') as f:
        lines = f.read().splitlines()

    data: list[tuple[int, list[int]]] = []
    for line in lines:
        parts = line.split(' ')
        target = int(parts[0][:-1])
        sources = [int(x) for x in parts[1:]]
        data.append((target, sources))
    return data


def is_achievable(target, sources):
    if len(sources) == 1:
        return target == sources[0]

    last_source = sources[-1]

    if target - last_source > 0:
        can_add = is_achievable(target - last_source, sources[:-1])
        if can_add:
            return True
    
    if target % last_source == 0:
        can_multiply = is_achievable(target // last_source, sources[:-1])
        if can_multiply:
            return True

    if str(target).endswith(str(last_source)):
        concat_candidate = int(str(target)[:-len(str(last_source))])
        can_concat = is_achievable(concat_candidate, sources[:-1])
        if can_concat:
            return True

    return False



def main(filename):
    data = parse_input(filename)
        
    total = 0
    for target, sources in data:
        if is_achievable(target, sources):
            total += target
    return total


r = main('input.txt')
print(f'answer: {r}')
