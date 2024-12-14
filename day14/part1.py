import re

def parse_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    return [
        map(int, re.match(pattern, line).groups())
        for line in lines
    ]
    

def main(filename: str, grid_width: int, grid_height: int):
    data = parse_input(f'day14/{filename}')

    steps = 100
    mid_width = (grid_width - 1) / 2
    mid_height = (grid_height - 1) / 2
    quadrants = [0, 0, 0, 0]

    for px, py, vx, vy in data:
        endx = (px + steps * vx) % grid_width
        endy = (py + steps * vy) % grid_height
        
        if endy < mid_height:
            if endx < mid_width:
                quadrants[0] += 1
            elif endx > mid_width:
                quadrants[1] += 1
        elif endy > mid_height:
            if endx < mid_width:
                quadrants[2] += 1
            elif endx > mid_width:
                quadrants[3] += 1

    total = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
    return total


assert main('sample.txt', 11, 7) == 12

r = main('input.txt', 101, 103)
print(f'answer: {r}')