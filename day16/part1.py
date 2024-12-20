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
    
    return min(v for k, v in distances.items() if k[0] == end_pos)

    

def main(filename: str):
    data = read_input(filename)
    r = algo(data)
    return r


assert main('sample.txt') == 7036
assert main('sample2.txt') == 11048
assert main('sample3.txt') == 21148
r = main('input.txt')
print(f'answer: {r}')