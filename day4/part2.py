with open('day4/input.txt') as f:
    data = f.read().splitlines()

def check_cell(data: list[list[str]], row: int, col: int):
    if data[row][col] != 'A':
        return False
    
    markers = [
        data[row - 1][col - 1],
        data[row - 1][col + 1],
        data[row + 1][col + 1],
        data[row + 1][col - 1],
    ]

    if not (markers.count('M') == 2 and markers.count('S') == 2):
        return False
    if markers[0] == markers[2]:
        return False
    
    return True

total = 0
for row in range(1, len(data) - 1):
    for col in range(1, len(data[row]) - 1):
        total += check_cell(data, row, col)
print(total)