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
        self.fences = []

    def expand_from(self, home_cell: Position):
        # print(f'expanding from {home_cell}')
        self.visited.append(home_cell)
        self.area += 1
        
        # perimeter_change = 0
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_cell = home_cell + Position(*direction)
            
            if next_cell in self.visited:
                continue
            # grid edge
            if next_cell.is_oob(self.data):
                self.fences.append((home_cell, direction))
                continue
            # region edge
            if next_cell.value(self.data) != home_cell.value(self.data):
                self.fences.append((home_cell, direction))
                continue

            self.expand_from(next_cell)

    def count_sides(self):
        y_axis = [(1, 0), (-1, 0)]
        x_axis = [(0, 1), (0, -1)]

        fences_identified = []
        sides = 0
        for fence in self.fences:
            if fence in fences_identified:
                continue

            pos, facing = fence
            continuous_edge_members = [fence]
            
            # facing left/right, check above/below, and vice versa
            if facing in y_axis:
                axis_to_search = x_axis
            else:
                axis_to_search = y_axis

            for direction in axis_to_search:
                # trace any connecting edges until no more found
                fence_pos = pos
                while True:
                    adjacent_pos = fence_pos + Position(*direction)
                    theoretical_fence = (adjacent_pos, facing)
                    if theoretical_fence in self.fences:
                        continuous_edge_members.append(theoretical_fence)
                        fence_pos = adjacent_pos
                    else:
                        break
            
            sides += 1
            fences_identified.extend(continuous_edge_members)

        return sides

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
                total += search.area * search.count_sides()
                visited.extend(search.visited)
    return total

sample_result = main('sample.txt')
assert sample_result == 1206, f'{sample_result = }'

answer = main('input.txt')
print(f'{answer = }')