from typing import NamedTuple, Self

class Position(NamedTuple):
    y: int
    x: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.y + other.y, self.x + other.x)

class Grid:
    def __init__(self, data: list[str]):
        self.data = data
        
        self.character_position = self.find_current_pos()

    def find_current_pos(self):
        for i, row in enumerate(self.data):
            if '@' in row:
                return Position(i, row.index('@'))
        raise Exception('could not find current position of @')

    def get_value(self, pos: Position):
        return self.data[pos.y][pos.x]
    
    def set_value(self, pos: Position, value: str):
        self.data[pos.y] = self.data[pos.y][:pos.x] + value + self.data[pos.y][pos.x + 1:]

    def move(self, direction: Position):
        pos = self.character_position
        boxes_to_affect = []
        while True:
            pos += direction
            value = self.get_value(pos)
            if value == '#':
                # consume step and keep grid the same
                # if not boxes_to_affect:
                #     # will bump into wall
                #     return
                # else:
                #     # will push boxes into wall
                #     return
                return
            elif value == '.':
                if not boxes_to_affect:
                    # will step into empty space
                    self.update_character_position(pos)
                    return
                else:
                    # will push boxes in this direction
                    # visually, the first box moves onto the open space we found
                    # all other boxes in between can stay put
                    self.update_character_position(boxes_to_affect[0])
                    self.set_value(pos, 'O')
                    return
            elif value == 'O':
                # will interact with a box
                boxes_to_affect.append(pos)

    def update_character_position(self, pos: Position):
        self.set_value(self.character_position, '.')
        self.set_value(pos, '@')
        self.character_position = pos

def parse_input(filename: str):
    with open(f'day15/{filename}') as f:
        data = f.read()
    
    grid, moves = data.split('\n\n')
    grid = grid.splitlines()
    moves = moves.replace('\n', '')

    return grid, moves

def main(filename: str):
    grid_data, moves = parse_input(filename)
    grid = Grid(grid_data)
    grid.find_current_pos()
    
    directions = {
        '^': Position(-1, 0),
        'v': Position(1, 0),
        '>': Position(0, 1),
        '<': Position(0, -1),
    }
    for move in moves:
        direction = directions[move]
        grid.move(direction)

    
    total = 0
    for i, row in enumerate(grid.data):
        for j, cell in enumerate(row):
            if cell == 'O':
                total += i * 100 + j
    return total


assert main('sample.txt') == 10092
assert main('sample2.txt') == 2028

r = main('input.txt')
print(f'answer: {r}')