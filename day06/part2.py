from collections import defaultdict
from copy import deepcopy


def find_start_pos(data: list[list[int]]):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == '^':
                return row, col
    raise Exception('bruh')

def get_col_as_list(data: list[list[str]], col: int):
    return [row[col] for row in data]

def get_indexes_of_obstacles(path: list):
    return [i for i, x in enumerate(path) if x == '#']

def get_next_collision(pos: int, obstacles: list[int], forward: bool):
    if forward:
        upcoming = [i for i in obstacles if i > pos]
    else:
        upcoming = list(reversed([i for i in obstacles if i < pos]))

    if not upcoming:
        return -1

    return upcoming[0]

def step_direction(direction: str, n: int = 1):
    seq = ['up', 'right', 'down', 'left']
    i = (seq.index(direction) + n) % len(seq)
    return seq[i]

def find_collision_up(data, pos):
    path = get_col_as_list(data, pos[1])
    obstacles = get_indexes_of_obstacles(path)
    collided_row = get_next_collision(pos[0], obstacles, forward=False)
    return collided_row

def find_collision_down(data, pos):
    path = get_col_as_list(data, pos[1])
    obstacles = get_indexes_of_obstacles(path)
    collided_row = get_next_collision(pos[0], obstacles, forward=True)
    return collided_row

def find_collision_left(data, pos):
    path = data[pos[0]]
    obstacles = get_indexes_of_obstacles(path)
    collided_col = get_next_collision(pos[1], obstacles, forward=False)
    return collided_col

def find_collision_right(data, pos):
    path = data[pos[0]]
    obstacles = get_indexes_of_obstacles(path)
    collided_col = get_next_collision(pos[1], obstacles, forward=True)
    return collided_col

def calculate_theoretical_collision(data, cell, direction):
    if direction == 'up':
        collided_row = find_collision_up(data, cell)
        collision = (collided_row, cell[1])
        new_pos = (collision[0] + 1, collision[1])
    elif direction == 'down':
        collided_row = find_collision_down(data, cell)
        collision = (collided_row, cell[1])
        new_pos = (collision[0] - 1, collision[1])
    elif direction == 'left':
        collided_col = find_collision_left(data, cell)
        collision = (cell[0], collided_col)
        new_pos = (collision[0], collision[1] + 1)
    elif direction == 'right':
        collided_col = find_collision_right(data, cell)
        collision = (cell[0], collided_col)
        new_pos = (collision[0], collision[1] - 1)
    return collision, new_pos



def run(data, pos, direction) -> bool:
    visited = defaultdict(list)
    collided = defaultdict(list)

    is_pos_oob = False
    while True:
        if direction == 'up':
            collided_row = find_collision_up(data, pos)
            if collided_row == -1:
                just_visited = [(row, pos[1]) for row in range(pos[0], -1, -1)]
                is_pos_oob = True
            else:
                new_pos = (collided_row + 1, pos[1])
                just_visited = [(row, pos[1]) for row in range(pos[0], new_pos[0] - 1, -1)]
                obstacle_pos = (collided_row, pos[1])
                collided[obstacle_pos].append(direction)
                if len(collided[obstacle_pos]) != len(set(collided[obstacle_pos])):
                    return visited, True

        elif direction == 'down':
            collided_row = find_collision_down(data, pos)
            if collided_row == -1:
                just_visited = [(row, pos[1]) for row in range(pos[0], len(data))]
                is_pos_oob = True
            else:
                new_pos = (collided_row - 1, pos[1])
                just_visited = [(row, pos[1]) for row in range(pos[0], new_pos[0] + 1)]
                obstacle_pos = (collided_row, pos[1])
                collided[obstacle_pos].append(direction)
                if len(collided[obstacle_pos]) != len(set(collided[obstacle_pos])):
                    return visited, True

        elif direction == 'left':
            collided_col = find_collision_left(data, pos)
            if collided_col == -1:
                just_visited = [(pos[0], col) for col in range(pos[1], -1, -1)]
                is_pos_oob = True
            else:
                new_pos = (pos[0], collided_col + 1)
                just_visited = [(pos[0], col) for col in range(pos[1], new_pos[1] - 1, -1)]
                obstacle_pos = (pos[0], collided_col)
                collided[obstacle_pos].append(direction)
                if len(collided[obstacle_pos]) != len(set(collided[obstacle_pos])):
                    return visited, True

        elif direction == 'right':
            collided_col = find_collision_right(data, pos)
            if collided_col == -1:
                just_visited = [(pos[0], col) for col in range(pos[1], len(data[0]))]
                is_pos_oob = True
            else:
                new_pos = (pos[0], collided_col - 1)
                just_visited = [(pos[0], col) for col in range(pos[1], new_pos[1] + 1)]
                obstacle_pos = (pos[0], collided_col)
                collided[obstacle_pos].append(direction)
                if len(collided[obstacle_pos]) != len(set(collided[obstacle_pos])):
                    return visited, True

        for cell in just_visited:
            visited[cell].append(direction)

        if is_pos_oob:
            return visited, False

        pos = new_pos
        direction = step_direction(direction)


def replace_at_coord(grid, pos, value):
    y, x = pos
    grid[y] = grid[y][:x] + value + grid[y][x + 1:]


with open('day06/input.txt') as f:
    data = f.read().splitlines()

start_pos = find_start_pos(data)
visited, is_looping = run(data, start_pos, 'up')

candidates = []
for cell in visited:
    if cell == start_pos:
        continue
    # make alternate version of map with a new obstacle
    alt_data = deepcopy(data)
    replace_at_coord(alt_data, cell, '#')
    # run it to see if it loops
    _, is_looping = run(alt_data, start_pos, 'up')
    if is_looping:
        candidates.append(cell)


# debugging
obstacle_count_bef = sum(row.count('#') for row in data)
print(f'{obstacle_count_bef = }')
for coord, passed_directions in visited.items():
    if len(passed_directions) == 1:
        if passed_directions[0] == 'left':
            c = '<'
        elif passed_directions[0] == 'right':
            c = '>'
        elif passed_directions[0] == 'up':
            c = '^'
        else:
            c = 'v'
    else:
        c = '+'
    replace_at_coord(data, coord, c)
for coord in candidates:
    replace_at_coord(data, coord, 'O')
for i, row in enumerate(data):
    print(f'{i+1:<3} | {row}')
obstacle_count_aft = sum(row.count('#') for row in data)
print(f'{obstacle_count_aft = }')
assert obstacle_count_bef == obstacle_count_aft, 'deleted some obstacles during traversal'

total = len(candidates) 
print(f'answer: {total}')
