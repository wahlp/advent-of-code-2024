from collections import defaultdict


def parse_input(filename):
    with open(f'day23/{filename}') as f:
        lines = f.read().splitlines()
    data = [line.split('-') for line in lines]
    return data


def parse_connections(data) -> dict[str, set]:
    connections = defaultdict(set)
    for com1, com2 in data:
        connections[com1].add(com2)
        connections[com2].add(com1)
    return connections


def find_common_neighbour(coms: list[str], connections: dict[str, set]):
    relevant_neighbours = [connections[com] for com in coms]
    return set.intersection(*relevant_neighbours)


def main(filename):
    data = parse_input(filename)
    connections = parse_connections(data)

    biggest_group = set()
    for com, connected_coms in connections.items():
        candidate_group = set()
        for candidate in connected_coms:
            potential_candidate_group = [com, candidate, *list(candidate_group)]
            common_neighbours = find_common_neighbour(potential_candidate_group, connections)
            if common_neighbours:
                candidate_group.add(candidate)

                # maybe the last member of the biggest group
                # no more neighbours to test against
                if len(common_neighbours) == 1:
                    last_member = list(common_neighbours)[0]
                    if connections[last_member].intersection(candidate_group) == candidate_group:
                        candidate_group.add(last_member)
        candidate_group.add(com)

        if len(candidate_group) > len(biggest_group):
            biggest_group = candidate_group
    
    return ','.join(sorted(list(biggest_group)))


assert main('sample.txt') == 'co,de,ka,ta'
r = main('input.txt')
print(f'answer: {r}')