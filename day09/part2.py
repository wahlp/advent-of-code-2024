with open('day09/input.txt') as f:
    data = f.read().replace('\n', '')

empty_char = '.'

block_id = 0
block_expr = []
blocks = {}
spaces = {}
for i, num_repeat in enumerate(data):
    num_repeat = int(num_repeat)
    if i % 2 == 0:
        blocks[block_id] = (len(block_expr), num_repeat)
        block_expr.extend([block_id] * num_repeat)
        block_id += 1
    else:
        spaces[len(block_expr)] = num_repeat
        block_expr.extend([empty_char] * num_repeat)

for block_id in reversed(blocks.keys()):
    block_loc, block_size = blocks[block_id]
    # update order after inserting in previous iteration
    spaces = dict(sorted(spaces.items()))

    space_loc = next(
        (space_loc for space_loc, space_size in spaces.items() if 0 < block_size <= space_size), -1
    )
    if space_loc == -1:
        continue
    # dont move to the right
    if space_loc > block_loc:
        continue
    # update block location
    blocks[block_id] = (space_loc, block_size)
    # shrink original space
    space_size = spaces[space_loc]
    spaces[space_loc] = 0
    spaces[space_loc + block_size] = space_size - block_size


s = [empty_char] * len(block_expr)
for block_id, (block_loc, block_size) in blocks.items():
    for i in range(block_loc, block_loc + block_size):
        s[i] = block_id

total = 0
for i, block_id in enumerate(s):
    if block_id != empty_char:
        total += block_id * i
print(f'{total = }')