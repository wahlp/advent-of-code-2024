from collections import Counter, defaultdict
from functools import cache


def read_input(filename: str):
    with open(f'day21/{filename}') as f:
        data = f.read().splitlines()
    return data

@cache
def calc_paths(pos1, pos2, illegal_pos, path_start = False):
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
    
    would_horizontally_enter_illegal_space = ((pos2[0] + dy, pos1[1] - dx) == illegal_pos)
    would_vertically_enter_illegal_space = ((pos1[0] - dy, pos2[1] + dx) == illegal_pos)

    vertical_first = y_component + x_component + 'A'
    horizontal_first = x_component + y_component + 'A'
    if would_horizontally_enter_illegal_space:
        return vertical_first
    if would_vertically_enter_illegal_space:
        return horizontal_first

    button_priority = ['<', '^v', '>A']
    diy = ''
    for button_set in button_priority:
        for button in button_set:
            diy += button * horizontal_first.count(button)
    return diy


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
def calc_numeric_button_code_path(code: str) -> str:
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
def calc_directional_button_code_path_members(prev_code_transitions: str):
    code_transitions = defaultdict(int)
    for i, (transition, count) in enumerate(prev_code_transitions.items()):
        c1 = DIRECTIONAL_KEYPAD[transition[0]]
        c2 = DIRECTIONAL_KEYPAD[transition[1]]
        subpath = calc_paths(c1, c2, (0, 0), i == 0)
        for k, v in convert_path_to_transitions(subpath).items():
            code_transitions[k] += v * count
    return code_transitions


def convert_path_to_transitions(path: str) -> dict[tuple[str, str], int]:
    path = 'A' + path
    transitions = [(path[i-1], path[i]) for i in range(len(path)) if i > 0]
    return Counter(transitions)


def parse_code(code, n):
    layer0 = calc_numeric_button_code_path(code)
    code_transitions = convert_path_to_transitions(layer0)
    for i in range(0, n):
        # print(f'calculating directional layer {i} for {code}')
        code_transitions = calc_directional_button_code_path_members(code_transitions)
    
    # complexity
    c1 = sum(v for v in code_transitions.values())
    c2 = int(code[:-1])
    return c1 * c2


def main(filename: str, layers: int):
    data = read_input(filename)
    total = 0
    for code in data:
        total += parse_code(code, layers)
    return total
    

assert main('sample.txt', 2) == 126384
r = main('input.txt', 25)
print(f'answer: {r}')