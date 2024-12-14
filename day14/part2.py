import re
from collections import defaultdict
from copy import deepcopy

def parse_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    return [
        list(map(int, re.match(pattern, line).groups()))
        for line in lines
    ]
    

def main(filename: str, grid_width: int, grid_height: int):
    data = parse_input(f'day14/{filename}')

    default_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for steps in range(10_000):
        grid = deepcopy(default_grid)
        
        # populate grid
        for px, py, vx, vy in data:
            endx = (px + steps * vx) % grid_width
            endy = (py + steps * vy) % grid_height
            grid[endy][endx] += 1

        # check if long continuous lines were formed
        longest_lines = defaultdict(int)
        for row in grid:
            lines = [0]
            for cell in row:
                if cell != 0:
                    lines[-1] += 1
                else:
                    # line ended
                    lines.append(0)
            longest_lines[max(lines)] += 1

        longest_long_line = max(longest_lines.keys())
        if longest_long_line < 10:
            continue
        if longest_lines[longest_long_line] == 2:
            print(f'found longest line of length {longest_long_line} at step {steps}')
            return steps

    raise Exception('bruh')

r = main('input.txt', 101, 103)
print(f'answer: {r}')