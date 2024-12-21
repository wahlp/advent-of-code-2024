

def read_input(filename: str):
    with open(f'day21/{filename}') as f:
        data = f.read().splitlines()
    return data


def calc_path(pos1, pos2, illegal_pos):
    dy = pos1[0] - pos2[0]
    dx = pos1[1] - pos2[1]

    if dy > 0:
        y_component = '^' * dy
    elif dy < 0:
        y_component = 'v' * abs(dy)
    else:
        y_component = ''
    
    if dx > 0:
        x_component = '<' * dx
    elif dx < 0:
        x_component = '>' * abs(dx)
    else:
        x_component = ''
    
    would_cross_illegal_space = (
        pos1[1] == illegal_pos[1] and pos2[0] == illegal_pos[0]
        # avoid vertical into horizontal crossing illegal space
    )
    if would_cross_illegal_space or ('<' in x_component and '^' in y_component):
        path = x_component + y_component
    else:
        path = y_component + x_component
    return path

NUMERIC_KEYPAD = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
}

def calc_numeric_button_code_path(code: str):
    pos = NUMERIC_KEYPAD['A']
    path = ''
    for c in code:
        path += calc_path(pos, NUMERIC_KEYPAD[c], (3, 0)) + 'A'
        pos = NUMERIC_KEYPAD[c]
    return path

DIRECTIONAL_KEYPAD = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}
def calc_directional_button_code_path(code: str):
    pos = DIRECTIONAL_KEYPAD['A']
    path = ''
    for c in code:
        path += calc_path(pos, DIRECTIONAL_KEYPAD[c], (0, 0)) + 'A'
        pos = DIRECTIONAL_KEYPAD[c]
    return path

def calc_complexity(button_presses: str, code: str):
   a = len(button_presses)
   b = int(''.join(c for c in code if c.isdigit()))
   return a * b

def parse_code(code):
    directional_code_1 = calc_numeric_button_code_path(code)
    directional_code_2 = calc_directional_button_code_path(directional_code_1)
    directional_code_3 = calc_directional_button_code_path(directional_code_2)
    return calc_complexity(directional_code_3, code)


def main(filename: str):
    data = read_input(filename)
    total = 0
    for code in data:
        total += parse_code(code)
    return total
    


# r = main('sample.txt')
# r = main('input.txt')
print(f'answer: {r}')