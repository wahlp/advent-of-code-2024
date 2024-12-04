with open('day4/input.txt') as f:
    data = f.read().splitlines()

def check_cell(data: list[list[str]], row: int, col: int):
    # count the number of XMAS occurrences starting on a coordinate position
    # strategy:
    # only look for X's to start the sequence
    # one X could start multiple XMAS occurrences
    if data[row][col] != 'X':
        return 0

    # find valid directions to check
    # there are 2 horizontal, 2 vertical, 4 diagonal
    # go clockwise from 12 o clock
    directions = [
        (0, -1),    # up
        (1, -1),    # up right
        (1, 0),     # right
        (1, 1),     # down right   
        (0, 1),     # down
        (-1, 1),    # down left
        (-1, 0),    # left
        (-1, -1)    # up left
    ]

    count = 0
    for direction in directions:
        # make sure going in that direction doesnt land us out of bounds
        if not validate_direction(data, row, col, direction):
            continue
        
        # this direction is now safe to check
        xpos, ypos = col, row
        s = 'X'
        for _ in range(3):
            dx, dy = direction
            xpos += dx
            ypos += dy
            s += data[ypos][xpos]
        if s == "XMAS":
            # print(f'found XMAS at {row = }, {col = }, {direction = }')
            count += 1
    
    return count

def validate_direction(data, row, col, direction):
    dx, dy = tuple(x * 3 for x in direction)
    return (
        0 <= row + dy < len(data) 
        and (0 <= col + dx < len(data[0]))
    )

total = 0
for row in range(len(data)):
    for col in range(len(data[row])):
        total += check_cell(data, row, col)

print(total)