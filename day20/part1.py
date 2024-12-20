from collections import defaultdict


def read_input(filename: str):
    with open(f'day20/{filename}') as f:
        grid = f.read().splitlines()
    
    start_pos = ()
    for i, row in enumerate(grid):
        s = row.find('S')
        if s > -1:
            start_pos = (i, s)

    return grid, start_pos


def algo(grid, start_pos):
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
    return distances


def get_reachable_from(pos, n=20):
    reachable = []
    for dy in range(-n, n + 1):
        leftover = n - abs(dy)
        for dx in range(-leftover, leftover + 1):
            reached = (pos[0] + dy, pos[1] + dx)
            reachable.append(reached)
    return reachable


def manhattan_distance(c1, c2):
    dy = abs(c1[0] - c2[0])
    dx = abs(c1[1] - c2[1])
    return dy + dx


def main(filename: str):
    grid, start_pos = read_input(filename)
    distances = algo(grid, start_pos)

    total = 0
    for cell in distances:
        reachables = get_reachable_from(cell, n=2)
        for reachable in reachables:
            if reachable not in distances:
                continue
            distance_saved = distances[reachable] - distances[cell] - manhattan_distance(cell, reachable)
            if distance_saved >= 100:
                total += 1
    return total


r = main('input.txt')
print(f'answer: {r}')