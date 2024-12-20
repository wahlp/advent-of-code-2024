from itertools import cycle


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


seq = cycle(['up', 'right', 'down', 'left'])
def direction_iterator():
    yield next(seq)


with open('day06/input.txt') as f:
    data = f.read().splitlines()

pos = find_start_pos(data)
visited = [pos]

while True:
    direction = next(direction_iterator())

    if direction == 'up':
        path = get_col_as_list(data, pos[1])
        obstacles = get_indexes_of_obstacles(path)
        collided_row = get_next_collision(pos[0], obstacles, forward=False)
        if collided_row == -1:
            visited.extend([(row, pos[1]) for row in range(pos[0], -1, -1)])
            break
        new_pos = (collided_row + 1, pos[1])
        visited.extend([(row, pos[1]) for row in range(pos[0], new_pos[0] - 1, -1)])

    elif direction == 'down':
        path = get_col_as_list(data, pos[1])
        obstacles = get_indexes_of_obstacles(path)
        collided_row = get_next_collision(pos[0], obstacles, forward=True)
        if collided_row == -1:
            visited.extend([(row, pos[1]) for row in range(pos[0], len(data))])
            break
        new_pos = (collided_row - 1, pos[1])
        visited.extend([(row, pos[1]) for row in range(pos[0], new_pos[0] + 1)])

    elif direction == 'left':
        path = data[pos[0]]
        obstacles = get_indexes_of_obstacles(path)
        collided_col = get_next_collision(pos[1], obstacles, forward=False)
        if collided_col == -1:
            visited.extend([(pos[0], col) for col in range(pos[1], -1, -1)])
            break
        new_pos = (pos[0], collided_col + 1)
        visited.extend([(pos[0], col) for col in range(pos[1], new_pos[1] - 1, -1)])

    elif direction == 'right':
        path = data[pos[0]]
        obstacles = get_indexes_of_obstacles(path)
        collided_col = get_next_collision(pos[1], obstacles, forward=True)
        if collided_col == -1:
            visited.extend([(pos[0], col) for col in range(pos[1], len(data[0]))])
            break
        new_pos = (pos[0], collided_col - 1)
        visited.extend([(pos[0], col) for col in range(pos[1], new_pos[1] + 1)])

    pos = new_pos

# debugging
obstacle_count_bef = sum(row.count('#') for row in data)
print(f'{obstacle_count_bef = }')
for coord in set(visited):
    data[coord[0]] = data[coord[0]][:coord[1]] + 'X' + data[coord[0]][coord[1] + 1:]
for i, row in enumerate(data):
    print(f'{i+1:<3} | {row}')
obstacle_count_aft = sum(row.count('#') for row in data)
print(f'{obstacle_count_aft = }')
assert obstacle_count_bef == obstacle_count_aft, 'deleted some obstacles during traversal'

total = len(set(visited))
print(total)
