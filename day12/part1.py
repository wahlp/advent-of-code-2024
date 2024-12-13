from typing import NamedTuple, Self


class Position(NamedTuple):
    y: int
    x: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.y + other.y, self.x + other.x)

    def value(self, data: list[list]):
        return data[self.y][self.x]

    def is_oob(self, data: list[list]):
        return not (0 <= self.y < len(data) and 0 <= self.x < len(data[0]))


class Search:
    def __init__(self, data: list[list]):
        self.data = data
        self.visited = []

        self.area = 0
        self.perimeter = 0

    def expand_from(self, home_cell: Position):
        # print(f'expanding from {home_cell}')
        self.visited.append(home_cell)
        self.area += 1
        
        perimeter_change = 0
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_cell = home_cell + Position(*direction)
            
            if next_cell in self.visited:
                continue
            # grid edge
            if next_cell.is_oob(self.data):
                perimeter_change += 1
                continue
            # region edge
            if next_cell.value(self.data) != home_cell.value(self.data):
                perimeter_change += 1
                continue

            self.expand_from(next_cell)

        self.perimeter += perimeter_change


def main(filename: str):
    with open(f'day12/{filename}') as f:
        data = f.read().splitlines()
    
    visited = []
    total = 0
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            if (y, x) not in visited:
                search = Search(data)
                search.expand_from(Position(y, x))
                # print(f'{search.area = :<3}, {search.perimeter = :<3}')
                total += search.area * search.perimeter
                visited.extend(search.visited)
    return total

sample_result = main('sample.txt')
assert sample_result == 1930, f'{sample_result = }'

answer = main('input.txt')
print(f'{answer = }')