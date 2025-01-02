from typing import NamedTuple, Self


class Position(NamedTuple):
    y: int
    x: int

    def __add__(self, other: Self) -> Self:
        return type(self)(self.y + other.y, self.x + other.x)
    
    def __sub__(self, other: Self) -> Self:
        return type(self)(self.y - other.y, self.x - other.x)


DIRECTIONS = [
    Position(-1, 0), 
    Position(0, 1), 
    Position(1, 0), 
    Position(0, -1)
]
def step_direction(direction: Position):
    i = (DIRECTIONS.index(direction) + 1) % 4
    return DIRECTIONS[i]


def parse_input(filename: str):
    with open(f"day06/{filename}") as f:
        return f.read().splitlines()


def get_jump_location(grid: list[list[str]], pos: Position, direction: Position):
    while grid[pos.y][pos.x] != "#":
        pos += direction

        # oob
        if not (0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[0])):
            return (pos, direction)

    pos -= direction
    direction = step_direction(direction)
    return (pos, direction)


def calc_jumps(grid: list[list[str]]):
    jumps: dict[tuple[Position, Position], tuple[Position, Position]] = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            pos = Position(y, x)
            for direction in DIRECTIONS:
                if grid[pos.y][pos.x] == '#':
                    continue
                jumps[(Position(y, x), direction)] = get_jump_location(grid, Position(y, x), direction)
    return jumps


def new_jump_using_block(block: Position, direction: Position):
    return (block - direction, step_direction(direction))


def jump(
    pos: Position, 
    direction: Position, 
    block: Position, 
    jump_map: dict[tuple[Position, Position], tuple[Position, Position]], 
):
    jump = jump_map.get((pos, direction))
    if jump is not None:
        fpos, _ = jump
        if (
            fpos.x == block.x and min(pos.y, fpos.y) <= block.y <= max(pos.y, fpos.y)
            or fpos.y == block.y and min(pos.x, fpos.x) <= block.x <= max(pos.x, fpos.x)
        ):
            return new_jump_using_block(block, direction)
        return jump
    return (None, None)

def get_full_path(grid: list[list[str]], start_pos: Position, direction: Position):
    pos = start_pos
    visited = set()
    while True:
        visited.add(pos)

        pos += direction
        if not (0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[0])):
            break
        if grid[pos.y][pos.x] == "#":
            pos -= direction
            direction = step_direction(direction)

    return visited


def path_loops_with_patch(block: Position, start_pos: Position, direction: Position, jump_map):
    pos = start_pos
    visited = set()
    while True:        
        pos, direction = jump(pos, direction, block, jump_map)
        if direction is None:
            return False

        if (pos, direction) in visited:
            return True

        visited.add((pos, direction))


def main(filename: str):
    grid = parse_input(filename)

    start_pos = next(
        Position(y, x) for y, row in enumerate(grid) for x, c in enumerate(row) if c == "^"
    )

    path = get_full_path(grid, start_pos, Position(-1, 0))

    valid_blocks = set()
    jumps = calc_jumps(grid)
    for block in path:
        if block != start_pos and path_loops_with_patch(block, start_pos, Position(-1, 0), jumps):
            valid_blocks.add(block)

    return len(valid_blocks)


# r = main('sample.txt')
r = main('input.txt')
print(f'answer = {r}')