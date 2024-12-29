EMPTY_CHAR = None

def parse_input(filename):
    with open(f'day09/{filename}') as f:
        data = f.read().replace('\n', '')

    block_id = 0
    block_expr = []
    for i, char in enumerate(data):
        if not block_expr:
            span = range(i, i + int(char))
        else:
            start = block_expr[-1][0].stop
            span = range(start, start + int(char))

        if i % 2 == 0:
            block_expr.append((span, block_id))
            block_id += 1
        else:
            block_expr.append((span, EMPTY_CHAR))
    return block_expr


def main(filename):
    block_expr = parse_input(filename)

    additions = 0
    for old_index, (span1, block_id1) in enumerate(reversed(block_expr)):
        old_index = len(block_expr) - old_index - additions - 1
        if block_id1 == EMPTY_CHAR:
            continue

        try:
            new_index = next(
                i for i, (span, block_id) in enumerate(block_expr) 
                if block_id == EMPTY_CHAR and len(span1) <= len(span) 
            )
        except StopIteration:
            continue

        span2 = block_expr[new_index][0]
        if span2.start > span1.start:
            # do not move to the right
            continue
        # found a legal move
        block_expr[old_index] = (span1, EMPTY_CHAR)
        block_expr[new_index] = (range(span2.start, span2.start + len(span1)), block_id1)
        if (diff := len(span2) - len(span1)) > 0:
            new_start = span2.start + len(span1)
            block_expr.insert(new_index + 1, (range(new_start, new_start + diff), EMPTY_CHAR))
            additions += 1

    # full_block_expr = ''.join(str(block_id) if block_id != EMPTY_CHAR else '.' for span, block_id in block_expr for _ in span)
    total = sum(sum(span) * block_id for span, block_id in block_expr if block_id != EMPTY_CHAR)
    return total


assert main('sample.txt') == 2858
r = main('input.txt')
print(f'answer = {r}')