with open('day09/input.txt') as f:
    data = f.read().replace('\n', '')

empty_char = None

block_id = 0
block_expr = []
for i, char in enumerate(data):
    num_repeat = int(char)
    if i % 2 == 0:
        block_expr.extend([block_id] * num_repeat)
        block_id += 1
    else:
        block_expr.extend([empty_char] * num_repeat)

while empty_char in block_expr:
    last = block_expr.pop()
    if last == empty_char:
        continue
    first_opening = block_expr.index(empty_char)
    block_expr[first_opening] = last

total = sum(i * int(char) for i, char in enumerate(block_expr))
print(f'{total = }')