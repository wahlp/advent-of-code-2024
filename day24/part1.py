def parse_input(filename: str):
    with open(f'day24/{filename}') as f:
        d1, d2 = f.read().split('\n\n')
    
    data1 = {}
    for line in d1.splitlines():
        k, v = line.split(': ')
        data1[k] = int(v)

    data2 = []
    for line in d2.splitlines():
        i1, op, i2, _, out = line.split()
        data2.append((i1, op, i2, out))
    
    return data1, data2


def main(filename: str):
    values, queue = parse_input(filename)

    while queue:
        statement = queue.pop(0)
        i1, op, i2, out = statement

        v1 = values.get(i1)
        v2 = values.get(i2)
        if v1 is None or v2 is None:
            queue.append(statement)
            continue

        if op == 'AND':
            values[out] = v1 & v2
        elif op == 'OR':
            values[out] = v1 | v2
        elif op == 'XOR':
            values[out] = v1 ^ v2
    
    bits = []
    for k, v in values.items():
        if k.startswith('z'):
            bitpos = int(k[1:])
            bits.append((bitpos, v))
    bits.sort(key=lambda x: x[0], reverse=True)
    answer = int(''.join(str(x[1]) for x in bits), 2)
    return answer


r = main('input.txt')
print(f'answer: {r}')