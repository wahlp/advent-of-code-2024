from typing import NamedTuple
class Position(NamedTuple):
    y: int
    x: int

class Search:
    def __init__(self, data: list[list[int]], start: Position):
        self.data = data
        self.pos = start
        self.found = []

    def run(self):
        self.explore(self.pos)
        return len(set(self.found))

    def explore(self, pos: Position):
        current_tile_value = self.data[pos.y][pos.x]

        adjacent_tiles = [
            Position(pos.y+1, pos.x),
            Position(pos.y-1, pos.x),
            Position(pos.y, pos.x+1),
            Position(pos.y, pos.x-1),
        ]
        for t in adjacent_tiles:
            if is_oob(self.data, t):
                continue

            adjacent_tile_value = self.data[t.y][t.x]
            if adjacent_tile_value == current_tile_value + 1:
                if adjacent_tile_value == 9:
                    self.found.append(t)
                else:
                    self.explore(t)

def is_oob(data: list[list], pos: Position):
    return not (
        0 <= pos.y < len(data)
        and 0 <= pos.x < len(data[0])
    )

def main():
    with open('day10/input.txt') as f:
        lines = f.read().splitlines()
    data = [[int(x) for x in row] for row in lines]
        
    start_positions = [
        Position(i, j) 
        for i, row in enumerate(data) 
        for j, val in enumerate(row) 
        if val == 0
    ]

    total = 0
    for start in start_positions:
        search = Search(data, start)
        r = search.run()
        # print(f'tree starting at {start} found {r}')
        total += r
    print(f'{total = }')

main()