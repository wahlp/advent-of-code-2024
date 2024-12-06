from collections import defaultdict


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


def get_next_direction(direction: str):
    seq = ['up', 'right', 'down', 'left']
    i = seq.index(direction) + 1
    if i == len(seq):
        i = 0
    return seq[i]


def get_next_cell(cell: tuple[int, int], direction: str):
    d = {
        'up':       (-1, 0),
        'right':    (0, 1),
        'down':     (1, 0),
        'left':     (0, -1),
    }
    return cell[0] + d[direction][0], cell[1] + d[direction][1]


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


with open('day6/input.txt') as f:
    data = f.read().splitlines()

pos = find_start_pos(data)
direction = 'up'
visited = defaultdict(list)
collided = defaultdict(list)
candidates = []

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
            collided[(collided_row, pos[1])].append(direction)

    elif direction == 'down':
        collided_row = find_collision_down(data, pos)
        if collided_row == -1:
            just_visited = [(row, pos[1]) for row in range(pos[0], len(data))]
            is_pos_oob = True
        else:
            new_pos = (collided_row - 1, pos[1])
            just_visited = [(row, pos[1]) for row in range(pos[0], new_pos[0] + 1)]
            collided[(collided_row, pos[1])].append(direction)

    elif direction == 'left':
        collided_col = find_collision_left(data, pos)
        if collided_col == -1:
            just_visited = [(pos[0], col) for col in range(pos[1], -1, -1)]
            is_pos_oob = True
        else:
            new_pos = (pos[0], collided_col + 1)
            just_visited = [(pos[0], col) for col in range(pos[1], new_pos[1] - 1, -1)]
            collided[(pos[0], collided_col)].append(direction)

    elif direction == 'right':
        collided_col = find_collision_right(data, pos)
        if collided_col == -1:
            just_visited = [(pos[0], col) for col in range(pos[1], len(data[0]))]
            is_pos_oob = True
        else:
            new_pos = (pos[0], collided_col - 1)
            just_visited = [(pos[0], col) for col in range(pos[1], new_pos[1] + 1)]
            collided[(pos[0], collided_col)].append(direction)

    # check for opportunities to create a loop
    next_direction = get_next_direction(direction)
    for cell in just_visited:
        # maybe a reachable cell to our clockwise 3oclock can be connected
        # check if we can to collide with an obstacle 
        # from an angle that has already been used
        if next_direction == 'up':
            collision_target = (find_collision_up(data, cell), cell[1])
            if collision_target in collided:
                if 'up' in collided[collision_target]:
                    candidates.append(get_next_cell(cell, direction))

        elif next_direction == 'down':
            collision_target = (find_collision_down(data, cell), cell[1])
            if collision_target in collided:
                if 'down' in collided[collision_target]:
                    candidates.append(get_next_cell(cell, direction))

        elif next_direction == 'left':
            collision_target = (cell[0], find_collision_left(data, cell))
            if collision_target in collided:
                if 'left' in collided[collision_target]:
                    candidates.append(get_next_cell(cell, direction))

        elif next_direction == 'right':
            collision_target = (cell[0], find_collision_right(data, cell))
            if collision_target in collided:
                if 'right' in collided[collision_target]:
                    candidates.append(get_next_cell(cell, direction))

        visited[cell].append(direction)
        # print(f'visited {cell = }')

    if is_pos_oob:
        break

    pos = new_pos
    direction = get_next_direction(direction)

# debugging
obstacle_count_bef = sum(row.count('#') for row in data)
print(f'{obstacle_count_bef = }')
for coord, passed_directions in visited.items():
    if len(passed_directions) == 1:
        if passed_directions[0] == 'left' or passed_directions[0] == 'right':
            c = '-'
        else:
            c = '|'
    else:
        c = '+'
    data[coord[0]] = data[coord[0]][:coord[1]] + c + data[coord[0]][coord[1] + 1:]
for coord in candidates:
    data[coord[0]] = data[coord[0]][:coord[1]] + 'O' + data[coord[0]][coord[1] + 1:]
for i, row in enumerate(data):
    print(f'{i+1:<3} | {row}')
obstacle_count_aft = sum(row.count('#') for row in data)
print(f'{obstacle_count_aft = }')
assert obstacle_count_bef == obstacle_count_aft, 'deleted some obstacles during traversal'

total = len(candidates) 
print(total)
