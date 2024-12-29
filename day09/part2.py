from collections import defaultdict
from heapq import heappop, heappush


EMPTY_CHAR = None

def parse_input(filename):
    with open(f'day09/{filename}') as f:
        data = f.read().replace('\n', '')

    blocks = []
    pos = 0
    spaces = defaultdict(list)
    for i, char in enumerate(data):
        block_size = int(char)
        block_range = range(pos, pos + block_size)
        if i % 2 == 0:
            block_id = i // 2
            blocks.append((block_range, block_id))
        else:
            heappush(spaces[block_size], pos)
        pos += block_size

    return blocks, spaces


def find_space(spaces, block_size, block_pos):
    best_pos = block_pos
    best_space_size = block_size
    for space_size in spaces.keys():
        if block_size > space_size:
            continue
        if spaces[space_size]:
            pos = spaces[space_size][0]
            if pos < best_pos:
                best_pos = pos
                best_space_size = space_size
    return best_pos, best_space_size



def main(filename):
    blocks, spaces = parse_input(filename)

    for i, (block_range, block_id) in enumerate(reversed(blocks)):
        block_size = len(block_range)
        space_pos, space_size = find_space(spaces, block_size, block_range.start)
        if space_pos == block_range.start:
            continue
        # legal move found
        heappop(spaces[space_size])
        blocks[len(blocks) - i - 1] = (range(space_pos, space_pos + block_size), block_id)
        if (space_leftover := space_size - block_size) > 0:
            heappush(spaces[space_leftover], space_pos + block_size)

    # full_block_expr = ''.join(str(block_id) if block_id != EMPTY_CHAR else '.' for span, block_id in blocks for _ in span)
    total = sum(sum(span) * block_id for span, block_id in blocks if block_id != EMPTY_CHAR)
    return total


assert main('sample.txt') == 2858
r = main('input.txt')
print(f'answer = {r}')