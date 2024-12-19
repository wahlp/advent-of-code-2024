from collections import defaultdict
from heapq import heappush, heappop


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
    for k in piece_appearances:
        piece_appearances[k].sort(key=lambda x: len(x))

    paths_to_pos = defaultdict(int)
    paths_to_pos[0] = 1
    queue = []
    heappush(queue, 0)
    while queue:
        start_pos = heappop(queue)
        candidates = piece_appearances[start_pos]
        for candidate in candidates:
            end_pos = start_pos + len(candidate)
            paths_to_pos[end_pos] += paths_to_pos[start_pos]
            if end_pos in piece_appearances and end_pos not in queue:
                heappush(queue, end_pos)
    return paths_to_pos[len(build)]


def main(filename):
    pieces, builds = parse_input(filename)
    pieces.sort(key=lambda x: len(x), reverse=True)

    total = 0    
    for build in builds:
        total += attempt_build(build, pieces)
    
    return total


assert main('sample.txt') == 16
r = main('input.txt')
print(f'answer: {r}')