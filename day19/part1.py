from collections import defaultdict


def parse_input(filename):
    with open(f'day19/{filename}') as f:
        pieces, _, *builds = f.read().splitlines()
    pieces = pieces.split(', ')
    return pieces, builds


def find_all(s: str, substr: str):
    i = s.find(substr)
    while i > -1:
        yield i
        i = s.find(substr, i + 1)


def attempt_build(build: str, pieces: list[str]):
    piece_appearances = defaultdict(list)
    for piece in pieces:
        for index in find_all(build, piece):
            piece_appearances[index].append(piece)

    queue = [0]
    while queue:
        pos = queue.pop(0)
        candidates = piece_appearances[pos]
        for item in candidates:
            next_item_pos = pos + len(item)
            if next_item_pos == len(build):
                return True
            if next_item_pos in piece_appearances and next_item_pos not in queue:
                queue.append((next_item_pos))
    return False



def main(filename):
    pieces, builds = parse_input(filename)
    pieces.sort(key=lambda x: len(x), reverse=True)

    total = 0    
    for build in builds:
        total += attempt_build(build, pieces)
    
    return total


assert main('sample.txt') == 6
r = main('input.txt')
print(f'answer: {r}')