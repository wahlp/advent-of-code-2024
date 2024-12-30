import re


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

    for steps in range(10_000):
        positions = []
        for px, py, vx, vy in data:
            endx = (px + steps * vx) % grid_width
            endy = (py + steps * vy) % grid_height
            positions.append((endx, endy))
        
        if len(positions) == len(set(positions)):
            return steps

r = main('input.txt', 101, 103)
print(f'answer: {r}')