def read_input(filename: str):
    with open(f'day21/{filename}') as f:
        data = f.read().splitlines()
    return data


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

    paths = []
    if not could_vertically_enter_illegal_space:
        paths.append(y_component + x_component + 'A')
    if not could_horizontally_enter_illegal_space:
        paths.append(x_component + y_component + 'A')
    return list(set(paths))

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

from itertools import product
def calc_numeric_button_code_path(code: str):
    pos = NUMERIC_KEYPAD['A']
    paths = []
    for c in code:
        subpaths = calc_paths(pos, NUMERIC_KEYPAD[c], (3, 0))
        if paths:
            paths = [''.join(path) for path in product(paths, subpaths)]
        else:
            paths = subpaths
        pos = NUMERIC_KEYPAD[c]
    return list(paths)

DIRECTIONAL_KEYPAD = {
    '^': (0, 1),
    'A': (0, 2),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
}
def calc_directional_button_code_path(code: str):
    pos = DIRECTIONAL_KEYPAD['A']
    paths = []
    for c in code:
        subpaths = calc_paths(pos, DIRECTIONAL_KEYPAD[c], (0, 0))
        if paths:
            paths = [''.join(path) for path in product(paths, subpaths)]
        else:
            paths = subpaths
        pos = DIRECTIONAL_KEYPAD[c]
    return paths


def calc_complexity(button_presses: str, code: str):
   a = len(button_presses)
   b = int(''.join(c for c in code if c.isdigit()))
   return a * b


def filter_shortest(a: list):
    if not a:
        return []
    shortest = len(min(a))
    return [x for x in a if len(x) == shortest]


def parse_code(code):
    codes_lv1 = calc_numeric_button_code_path(code)
    codes_lv1 = filter_shortest(codes_lv1)

    codes_lv2 = []
    for code_lv1 in codes_lv1:
        codes_lv2.extend(calc_directional_button_code_path(code_lv1))
    codes_lv2 = filter_shortest(codes_lv2)
    
    codes_lv3 = []
    for code_lv2 in codes_lv2:
        codes_lv3.extend(calc_directional_button_code_path(code_lv2))
    codes_lv3 = filter_shortest(codes_lv3)
    
    return calc_complexity(codes_lv3[0], code)


def main(filename: str):
    data = read_input(filename)
    total = 0
    for code in data:
        total += parse_code(code)
    return total
    

# r = main('sample.txt')
r = main('input.txt')
print(f'answer: {r}')