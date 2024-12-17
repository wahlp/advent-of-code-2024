from queue import Queue
from typing import NamedTuple


class Connections(NamedTuple):
    up: bool
    down: bool
    left: bool
    right: bool


class Intersection(NamedTuple):
    y: int
    x: int
    connections: Connections

class Node:
    def __init__(self, pos):
        self.pos = pos
        self.neighbours: list[tuple[int, str, Node]] = []

    def add_neighbour(self, distance, direction, other):
        self.neighbours.append((distance, direction, other))


def read_input(filename: str):
    with open(f'day16/{filename}') as f:
        data = f.read().replace('S', '.').replace('E', '.').splitlines()
    return data


def find_intersections(data: list[str]):
    intersections: list[Intersection] = []
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == '#':
                continue

            up = data[i-1][j]
            down = data[i+1][j]
            left = data[i][j-1]
            right = data[i][j+1]

            connections = Connections(*(x == '.' for x in (up, down, left, right)))
            num_connections = sum(connections)
            if num_connections == 2:
                if left == right:
                    # corridor cell, not an intersection
                    continue

            intersections.append(Intersection(i, j, connections))
    return intersections

def parse_nodes(intersections: list[Intersection]) -> dict[tuple[int, int], Node]:
    nodes = {}
    for intersection in intersections:
        pos = (intersection.y, intersection.x)
        if pos not in nodes:
            nodes[pos] = Node(pos)
        node = nodes[pos]

        for direction, connection_exists in intersection.connections._asdict().items():
            if connection_exists:
                if direction == 'up':
                    d = [x for x in intersections if x.x == intersection.x and x.y < intersection.y]
                    d.sort(key=lambda x: x.y, reverse=True)
                elif direction == 'down':
                    d = [x for x in intersections if x.x == intersection.x and x.y > intersection.y]
                    d.sort(key=lambda x: x.y)
                elif direction == 'left':
                    d = [x for x in intersections if x.y == intersection.y and x.x < intersection.x]
                    d.sort(key=lambda x: x.x, reverse=True)
                else:
                    # right
                    d = [x for x in intersections if x.y == intersection.y and x.x > intersection.x]
                    d.sort(key=lambda x: x.x)
                
                connected = d[0]
                connected_pos = (connected.y, connected.x)
                if direction == 'up' or direction == 'down':
                    distance = abs(intersection.y - connected.y)
                else:
                    distance = abs(intersection.x - connected.x)

                if connected_pos not in nodes:
                    nodes[connected_pos] = Node(connected_pos)
                connected_node = nodes[connected_pos]
                node.add_neighbour(distance, direction, connected_node)
    return nodes


DIRECTIONS = ['up', 'right', 'down', 'left']
def calc_turns(direction1: str, direction2: str):
    turns = abs(DIRECTIONS.index(direction1) - DIRECTIONS.index(direction2))
    if turns == 3:
        turns = 1
    return turns

class Algo:
    def __init__(self, nodes: list[Node]):
        self.distances: dict[tuple[int, int], dict[str, int]] = {}
        self.visited: dict[tuple[int, int], bool] = {}
        for pos in nodes:
            self.distances[pos] = {}
            for direction in DIRECTIONS:
                self.distances[pos][direction] = float('inf')
            self.visited[pos] = False
    
    def start(self, start_node: Node):
        self.distances[start_node.pos]['right'] = 0
        q = Queue()
        q.put((start_node, 'right'))
        while not q.empty():
            node, exit_facing = q.get()
            self.visited[node.pos] = True
            for distance, enter_facing, neighbour in node.neighbours:
                # different entry direction will result in different cost
                # this might propagate different costs down, so keep note
                for entry_facing_for_node_cost, node_cost in self.distances[node.pos].items():
                    if node_cost == float('inf'):
                        continue
                    turns = calc_turns(entry_facing_for_node_cost, enter_facing)
                    total_cost = node_cost + distance + turns * 1000
                    if total_cost < self.distances[neighbour.pos][enter_facing]:
                        self.distances[neighbour.pos][enter_facing] = total_cost
                if self.visited[neighbour.pos] is False:
                    q.put((neighbour, enter_facing))


def main(filename: str):
    data = read_input(filename)

    intersections = find_intersections(data)
    nodes = parse_nodes(intersections)
    
    start_pos = (len(data) - 2, 1)
    end_pos = (1, len(data[0]) - 2)
    
    # for connection in nodes[start_pos].neighbours:
    algo = Algo(nodes)
    algo.start(nodes[start_pos])
    r = min(algo.distances[end_pos].values())

    return r


assert main('sample.txt') == 7036
r = main('input.txt')
print(f'answer: {r}')