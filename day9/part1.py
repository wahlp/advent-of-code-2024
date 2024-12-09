with open('day9/input.txt') as f:
    data = f.read().replace('\n', '')

block_id = 0
s = ''
for i, char in enumerate(data):
    if i % 2 == 0:
        s += str(block_id) * int(char)
        block_id += 1
    else:
        s += '.' * int(char)

# print(s)

block_expr = list(s)
while '.' in block_expr:
    last = block_expr.pop()
    if last == '.':
        continue
    first_opening = block_expr.index('.')
    block_expr[first_opening] = last

# print(''.join(block_expr))

total = 0
for i, char in enumerate(block_expr):
    total += i * int(char)
print(f'{total = }')