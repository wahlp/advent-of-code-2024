from itertools import product

def parse_input(filename: str):
    with open(f'day25/{filename}') as f:
        segments = f.read().split('\n\n')
    
    locks = []
    keys = []
    for segment in segments:
        shape = segment.splitlines()
        if all(x == '#' for x in shape[0]):
            locks.append(convert_to_heights(shape))
        else:
            keys.append(convert_to_heights(shape))
    return locks, keys


def convert_to_heights(shape):
    counts = []
    for col in range(len(shape[0])):
        count = sum(row[col] == '#' for row in shape)
        counts.append(count)
    return counts


def main(filename: str):
    locks, keys = parse_input(filename)

    count = 0
    for lock, key in product(locks, keys):
        count += all(lock_col + key_col <= 7 for lock_col, key_col in zip(lock, key))
    return count


r = main('input.txt')
print(f'answer: {r}')