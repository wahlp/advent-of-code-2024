from collections import defaultdict
from copy import deepcopy


def read_input(filename: str):
    with open(f'day20/{filename}') as f:
        grid = f.read().splitlines()
    
    start_pos = ()
    end_pos = ()
    walls = []
    for i, row in enumerate(grid):
        s = row.find('S')
        if s > -1:
            start_pos = (i, s)
        e = row.find('E')
        if e > -1:
            end_pos = (i, e)
        for h in find_all(row, '#'):
            walls.append((i, h))

    return grid, start_pos, end_pos, walls


def find_all(s: str, substr: str):
    i = s.find(substr)
    while i > -1:
        yield i
        i = s.find(substr, i + 1)


def algo(grid, start_pos, end_pos):

    distances = defaultdict(lambda: 1e9)
    distances[start_pos] = 0
    visited = defaultdict(lambda: False)
    queue = [start_pos]
    while queue:
        pos = queue.pop(0)
        visited[pos] = True
        for neighbour in [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]:
            ny, nx = neighbour
            if neighbour in visited:
                continue
            # oob
            if not (0 <= ny < len(grid) and 0 <= nx < len(grid[0])):
                continue
            if grid[ny][nx] == '#':
                visited[pos] = True
                continue
            distances[neighbour] = distances[pos] + 1
            queue.append(neighbour)
    return distances[end_pos]

def mod_grid(grid, wall):
    y, x = wall
    grid[y] = grid[y][:x] + '.' + grid[y][x+1:]
    return grid


def main(filename: str):
    grid, start_pos, end_pos, walls = read_input(filename)
    baseline = algo(grid, start_pos, end_pos)

    total = 0
    for wall in walls:
        modded_grid = mod_grid(deepcopy(grid), wall)
        modded_result = algo(modded_grid, start_pos, end_pos)
        if baseline - modded_result >= 100:
            total += 1
    return total


r = main('input.txt')
print(f'answer: {r}')