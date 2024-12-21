from functools import cache


def read_input(filename: str):
    with open(f'day21/{filename}') as f:
        data = f.read().splitlines()
    return data

@cache
def calc_paths(pos1, pos2, illegal_pos):
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
    
    could_vertically_enter_illegal_space = (
        pos1[1] == illegal_pos[1] and pos2[0] == illegal_pos[0]
    )
    could_horizontally_enter_illegal_space = (
        pos2[1] == illegal_pos[1] and pos1[0] == illegal_pos[0]
    )

    if not could_vertically_enter_illegal_space:
        # <^ results in shorter code later on than ^<
        if (
            not could_horizontally_enter_illegal_space 
            and ('<' in x_component and '^' in y_component)
        ):
            path = x_component + y_component + 'A'
        else:
            path = y_component + x_component + 'A'
    elif not could_horizontally_enter_illegal_space:
        path = x_component + y_component + 'A'

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
        path += calc_paths(pos, NUMERIC_KEYPAD[c], (3, 0))
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
        path += calc_paths(pos, DIRECTIONAL_KEYPAD[c], (0, 0))
        pos = DIRECTIONAL_KEYPAD[c]
    return path


def calc_complexity(code: str, processed_code: str):
   a = len(processed_code)
   b = int(code[:-1])
   return a * b


def parse_code(code, n):
    code_layers = [calc_numeric_button_code_path(code)]
    for i in range(1, n):
        print(f'calculating directional layer {i}')
        processed_code = calc_directional_button_code_path(code_layers[-1])
        code_layers.append(processed_code)
    
    return calc_complexity(code, processed_code)


def main(filename: str, layers: int):
    data = read_input(filename)
    total = 0
    for code in data:
        total += parse_code(code, layers)
    return total
    

assert main('sample.txt', 3) == 126384
r = main('input.txt', 3)
print(f'answer: {r}')