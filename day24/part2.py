from copy import deepcopy


def parse_input(filename: str):
    with open(f'day24/{filename}') as f:
        d1, d2 = f.read().split('\n\n')
    
    data1 = {}
    for line in d1.splitlines():
        k, v = line.split(': ')
        data1[k] = int(v)

    data2 = {}
    for line in d2.splitlines():
        i1, op, i2, _, out = line.split()
        data2[out] = [i1, op, i2]
    
    return data1, data2


def binary_digits_list_to_int(lst: list[int]):
    lst.reverse()
    s = ''.join(str(x) for x in lst)
    return int(s, 2)


def compare_z_output_to_expected(expected_z_bits, values):
    different_indexes = []
    num_bits = len(expected_z_bits)
    for i in range(num_bits):
        actual_bits_place = num_bits - i - 1
        pos = str(actual_bits_place).rjust(2, '0')
        actual_z_bit = str(values[f'z{pos}'])
        if expected_z_bits[i] != actual_z_bit:
            different_indexes.append(actual_bits_place)
    return different_indexes

def calc_expected_z(values: dict[str, int]):
    x_bits = [None] * 45
    y_bits = [None] * 45
    for k, v in values.items():
        if k.startswith('x'):
            pos = int(k[1:])
            x_bits[pos] = v
        elif k.startswith('y'):
            pos = int(k[1:])
            y_bits[pos] = v

    x_val = binary_digits_list_to_int(x_bits)
    y_val = binary_digits_list_to_int(y_bits)
    return x_val + y_val


def apply_swaps(swaps, stmt_dict):
    for a, b in swaps:
        stmt_dict[a], stmt_dict[b] = stmt_dict[b], stmt_dict[a]
    return stmt_dict



def make_digit(letter: str, num: int):
    return letter + str(num).rjust(2, '0')


def make_variations(input1: str, operator: str, input2: str):
    return [
        [input1, operator, input2],
        [input2, operator, input1]
    ]


def main(filename: str):
    inputs, statements_dict = parse_input(filename)
    expected_z_bits = bin(calc_expected_z(inputs))[2:]

    swaps = []
    digit_to_check = 1
    while True:
        changed_statements = apply_swaps(swaps, deepcopy(statements_dict))
        values = eval_statements(deepcopy(inputs), changed_statements)
        wrong_digits = compare_z_output_to_expected(expected_z_bits, values)

        if not wrong_digits:
            break

        swap = find_swap(digit_to_check, changed_statements)
        if swap is not None:
            swaps.append(swap)
        digit_to_check += 1

    return ','.join(sorted(x for tup in swaps for x in tup))


def find_swap(wrong_digit: int, statements_dict: dict):
    potential_swap = set()

    z_digit = make_digit('z', wrong_digit)
    if statements_dict[z_digit][1] != 'XOR':
        potential_swap.add(z_digit)

    x_digit = make_digit('x', wrong_digit)
    y_digit = make_digit('y', wrong_digit)

    xy_and_statements = make_variations(x_digit, 'AND', y_digit)
    xy_and = next(k for k, v in statements_dict.items() if v in xy_and_statements)
    # (x and y) should feed into or with ((x xor y) and carry)
    xy_and_child = {k: v for k, v in statements_dict.items() if xy_and in v} 
    if len(xy_and_child) != 1:
        # something wrong with xy_and's target
        potential_swap.add(xy_and)
        if len(potential_swap) == 2:
            return tuple(potential_swap)

    xy_xor_statements = make_variations(x_digit, 'XOR', y_digit)
    xy_xor = next(k for k, v in statements_dict.items() if v in xy_xor_statements)
    # (x xor y) should feed into another xor / and with carry
    xy_xor_children = {k: v for k, v in statements_dict.items() if xy_xor in v}
    if len(xy_xor_children) != 2:
        potential_swap.add(xy_xor)
        if len(potential_swap) == 2:
            return tuple(potential_swap)
    else:
        for xy_xor_child, xy_xor_child_statement in xy_xor_children.items():
            if xy_xor_child_statement[1] == 'XOR':
                if xy_xor_child != z_digit:
                    potential_swap.add(xy_xor_child)
                    if len(potential_swap) == 2:
                        return tuple(potential_swap)


def eval_statements(inputs, statements_dict):
    queue = [[*v, k] for k, v in statements_dict.items()]
    while queue:
        statement = queue.pop(0)
        i1, op, i2, out = statement

        v1 = inputs.get(i1)
        v2 = inputs.get(i2)
        if v1 is None or v2 is None:
            queue.append(statement)
            continue

        if op == 'AND':
            inputs[out] = v1 & v2
        elif op == 'OR':
            inputs[out] = v1 | v2
        elif op == 'XOR':
            inputs[out] = v1 ^ v2
    return inputs

r = main('input.txt')
print(f'answer: {r}')