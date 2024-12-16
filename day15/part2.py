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
        cells_to_affect: list[Position] = []
        while True:
            pos += direction
            value = self.get_value(pos)
            if value in ('[', ']'):
                # pushing box
                cells_to_affect.append(pos)
            elif value == '#':
                # pushing into wall, dont update anything
                return
            elif value == '.':
                if not cells_to_affect:
                    # will step into empty space
                    self.update_character_position(pos)
                    return
                else:
                    # will push boxes
                    break
        
        if direction.y == 0:
            # left/right
            for cell_pos in reversed(cells_to_affect):
                v = self.get_value(cell_pos)
                self.set_value(cell_pos + direction, v)
                self.set_value(cell_pos, '.')
            self.update_character_position(self.character_position + direction)
        else:
            # up/down
            first_box_half = cells_to_affect[0]
            # check further for any box pieces
            # if any of them would be pushed into a wall, abort all pushes
            is_valid_push, vertically_affected_cells = self.check_vertical(first_box_half, direction, [])
            if is_valid_push is False:
                return
            # if searching up, sort topmost cells first
            # if searching down, sort bottommost cells first
            vertically_affected_cells.sort(key=lambda x: x.y, reverse=(direction.y == 1))
            for cell_pos in vertically_affected_cells:
                v = self.get_value(cell_pos)
                self.set_value(cell_pos + direction, v)
                self.set_value(cell_pos, '.')
            self.update_character_position(self.character_position + direction)


    def check_vertical(self, start_pos: Position, direction: Position, affected_cells: list[Position]) -> tuple[bool, list[Position]]:
        # recursively check for free spaces to push into
        # and keep track of which cells needs to be pushed
        v = self.get_value(start_pos)
        if v == '#':
            return False, affected_cells
        elif v == '.':
            return True, affected_cells
        elif v == '[':
            # connecting ] piece
            connected_piece = start_pos + Position(0, 1)
        else:
            # connecting [
            connected_piece = start_pos + Position(0, -1)

        for cell in (start_pos + direction, connected_piece + direction):
            is_valid_push, affected_cells = self.check_vertical(cell, direction, affected_cells)
            if is_valid_push is False:
                return False, affected_cells
            
        for cell in (start_pos, connected_piece):
            if cell not in affected_cells:
                affected_cells.append(cell)
        return True, affected_cells


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

    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == '#':
                new_cell = '##'
            elif cell == 'O':
                new_cell = '[]'
            elif cell == '.':
                new_cell = '..'
            elif cell == '@':
                new_cell = '@.'
            new_row.append(new_cell)
        new_grid.append(''.join(new_row))

    return new_grid, moves

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
            if cell == '[':
                    total += i * 100 + j
    return total


# main('sample3.txt')
assert main('sample.txt') == 9021

r = main('input.txt')
print(f'answer: {r}')