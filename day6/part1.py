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
        upcoming = [i for i in obstacles if i < pos]

    if not upcoming:
        return -1
    if forward:
        return upcoming[0]
    else:
        return upcoming[-1]


with open('day6/input.txt') as f:
    data = f.read().splitlines()

pos = find_start_pos(data)
direction = 'up'
visited = [pos]

while True:
    if direction == 'up':
        path = get_col_as_list(data, pos[1])
        obstacles = get_indexes_of_obstacles(path)
        collided_row = get_next_collision(pos[0], obstacles, forward=False)
        if collided_row == -1:
            visited.extend([(row, pos[1]) for row in range(pos[0], -1, -1)])
            break
        new_pos = (collided_row + 1, pos[1])
        visited.extend([(row, pos[1]) for row in range(pos[0], new_pos[0] - 1, -1)])
        direction = 'right'

    elif direction == 'down':
        path = get_col_as_list(data, pos[1])
        obstacles = get_indexes_of_obstacles(path)
        collided_row = get_next_collision(pos[0], obstacles, forward=True)
        if collided_row == -1:
            visited.extend([(row, pos[1]) for row in range(pos[0], len(data))])
            break
        new_pos = (collided_row - 1, pos[1])
        visited.extend([(row, pos[1]) for row in range(pos[0], new_pos[0] + 1)])
        direction = 'left'

    elif direction == 'left':
        path = data[pos[0]]
        obstacles = get_indexes_of_obstacles(path)
        collided_col = get_next_collision(pos[1], obstacles, forward=False)
        if collided_col == -1:
            visited.extend([(pos[0], col) for col in range(pos[1], -1, -1)])
            break
        new_pos = (pos[0], collided_col + 1)
        visited.extend([(pos[0], col) for col in range(pos[1], new_pos[1] - 1, -1)])
        direction = 'up'

    elif direction == 'right':
        path = data[pos[0]]
        obstacles = get_indexes_of_obstacles(path)
        collided_col = get_next_collision(pos[1], obstacles, forward=True)
        if collided_col == -1:
            visited.extend([(pos[0], col) for col in range(pos[1], len(data[0]))])
            break
        new_pos = (pos[0], collided_col - 1)
        visited.extend([(pos[0], col) for col in range(pos[1], new_pos[1] + 1)])
        direction = 'down'

    pos = new_pos

# debugging
obstacle_count = sum(row.count('#') for row in data)
print(f'{obstacle_count = }')
for coord in set(visited):
    data[coord[0]] = data[coord[0]][:coord[1]] + 'X' + data[coord[0]][coord[1] + 1:]
for i, row in enumerate(data):
    print(f'{i:<3} | {row}')
obstacle_count = sum(row.count('#') for row in data)
print(f'{obstacle_count = }')

total = len(set(visited))
print(total)
