from collections import defaultdict

def read_input(filename: str):
    with open(f'day16/{filename}') as f:
        data = f.read().replace('S', '.').replace('E', '.').splitlines()
    return data


def move_forward(pos, direction):
    if direction == 'up':
        return (pos[0] - 1, pos[1])
    elif direction == 'down':
        return (pos[0] + 1, pos[1])
    elif direction == 'left':
        return (pos[0], pos[1] - 1)
    else:
        return (pos[0], pos[1] + 1)


def rotate_direction(direction, n):
    directions = ['right', 'down', 'left', 'up']
    i = (directions.index(direction) + n) % 4
    return directions[i]


def algo(grid: list[str]):
    start_pos = (len(grid) - 2, 1)
    end_pos = (1, len(grid[0]) - 2)

    start_params = (start_pos, 'right') 
    distances = defaultdict(lambda: 1e9)
    distances[start_params] = 0
    queue = [start_params]
    while queue:
        pos, direction = queue.pop(0)
        # move forward or rotate
        for npos, ndir, distance in [
            (move_forward(pos, direction), direction, 1), 
            (pos, rotate_direction(direction, 1), 1000), 
            (pos, rotate_direction(direction, 3), 1000)
        ]:
            if grid[npos[0]][npos[1]] == '#':
                continue

            new_distance = distances[(pos, direction)] + distance
            if new_distance < distances[(npos, ndir)]:
                distances[(npos, ndir)] = new_distance
                queue.append((npos, ndir))
    
    return find_members_of_shortest_paths(distances, start_pos, end_pos)


def find_members_of_shortest_paths(distances, start_pos, end_pos):
    positions_with_data = set(x[0] for x in distances.keys())
    end_pos_lowest_value = min(v for k, v in distances.items() if k[0] == end_pos)
    end_pos_entry_direction = next(k for k, v in distances.items() if v == end_pos_lowest_value)[1]

    visited = set()
    queue = [(end_pos, end_pos_entry_direction)]
    while queue:
        pos_aft, direction_aft = queue.pop(0)
        visited.add(pos_aft)
        if pos_aft == start_pos:
            continue
        prev_positions = find_possible_previous_positions(pos_aft)
        for pos_bef, direction_bef in prev_positions:
            if pos_bef not in positions_with_data:
                continue
            if pos_bef in visited:
                continue
            if distances[pos_bef, direction_bef] > end_pos_lowest_value:
                continue
            # reverse the calculation and see if it was possible to come from here
            if validate_move(distances, pos_bef, direction_bef, pos_aft, direction_aft):
                queue.append((pos_bef, direction_bef))
    return visited

def find_possible_previous_positions(pos):
    return [
        ((pos[0] + 1, pos[1]), 'up'),
        ((pos[0] - 1, pos[1]), 'down'),
        ((pos[0], pos[1] + 1), 'left'),
        ((pos[0], pos[1] - 1), 'right'),
    ]

def validate_move(distances, pos_bef, direction_bef, pos_aft, direction_aft):
    a = (
        distances[(pos_bef, direction_bef)] + 1
        == distances[(pos_aft, direction_bef)]
    ) 
    if direction_bef != direction_aft:
        b = (
            # make sure moving forward + turning is part of one solution
            # and not two separate solutions
            distances[(pos_aft, direction_bef)] + 1000
            == distances[(pos_aft, direction_aft)]
        )
        return a and b
    else:
        return a


def print_grid(data, visited):
    for i, line in enumerate(data):
        new_line = ''
        for j in range(len(line)):
            if (i, j) in visited:
                new_line += 'O'
            else:
                new_line += line[j]
        print(new_line)

def main(filename: str):
    data = read_input(filename)
    visited = algo(data)
    print_grid(data, visited)
    return len(visited)


assert main('sample.txt') == 45
assert main('sample2.txt') == 64
# assert main('sample3.txt') == 21148
r = main('input.txt')
print(f'answer: {r}')