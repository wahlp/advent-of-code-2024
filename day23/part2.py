from collections import defaultdict


def parse_input(filename):
    with open(f'day23/{filename}') as f:
        lines = f.read().splitlines()
    
    connections = defaultdict(set)
    for line in lines:
        com1, com2 = line.split('-')
        connections[com1].add(com2)
        connections[com2].add(com1)
    return connections


def bron_kerbosch(
    R: set[str],
    P: set[str],
    X: set[str],
    connections: dict[str, set[str]],
    cliques: list[set[str]],
):
    if not P and not X:
        cliques.append(R)
        return

    u = next(iter(P | X))
    for v in P - connections[u]:
        bron_kerbosch(R | {v}, P & connections[v], X & connections[v], connections, cliques)
        P.remove(v)
        X.add(v)


def main(filename):
    connections = parse_input(filename)

    cliques = []
    bron_kerbosch(set(), set(connections.keys()), set(), connections, cliques)
    biggest_clique = max(cliques, key=len) 
    return ','.join(sorted(list(biggest_clique)))


r = main('input.txt')
print(f'answer: {r}')