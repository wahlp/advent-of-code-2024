EMPTY_CHAR = None

def parse_input(filename):
    with open(f'day09/{filename}') as f:
        data = f.read().replace('\n', '')

    block_id = 0
    block_expr = []
    for i, char in enumerate(data):
        if i % 2 == 0:
            block_expr.extend([block_id] * int(char))
            block_id += 1
        else:
            block_expr.extend([EMPTY_CHAR] * int(char))
    return block_expr


def main(filename):
    block_expr = parse_input(filename)
    # turning point will be the final length of the compressed characters string
    turning_point = sum(x != EMPTY_CHAR for x in block_expr)
    
    # fold it at the turning point
    chars_right = iter(x for x in reversed(block_expr[turning_point:]) if x != EMPTY_CHAR)
    new_block_expr = [EMPTY_CHAR] * turning_point
    for i in range(turning_point):
        if block_expr[i] == EMPTY_CHAR:
            new_block_expr[i] = next(chars_right)
        else:
            new_block_expr[i] = block_expr[i]

    total = sum(i * int(char) for i, char in enumerate(new_block_expr))
    return total


assert main('sample.txt') == 1928
r = main('input.txt')
print(f'answer = {r}')