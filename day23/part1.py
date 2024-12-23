from collections import defaultdict


def parse_input(filename):
    with open(f'day23/{filename}') as f:
        lines = f.read().splitlines()
    data = [line.split('-') for line in lines]
    return data


def main(filename):
    data = parse_input(filename)

    triangles: list[set] = []
    connections = defaultdict(set)
    for com1, com2 in data:
        connections[com1].add(com2)
        connections[com2].add(com1)

        intersect = connections[com1].intersection(connections[com2])
        if intersect:
            for com3 in intersect:
                triangle = set([com1, com2, com3])
                triangles.append(triangle)
    
    count = 0
    for triangle in triangles:
        if any(com.startswith('t') for com in triangle):
            count += 1
    return count


assert main('sample.txt') == 7
r = main('input.txt')
print(f'answer: {r}')