from functools import cache

@cache
def eval_stone(value: int):
    if value == 0:
        return [1]
    
    v = str(value)
    if len(v) % 2 == 0:
        mid = len(v) // 2
        return [int(v[:mid]), int(v[mid:])]
    
    return [value * 2024]

from collections import Counter, defaultdict
def main():
    with open('day11/input.txt') as f:
        data = list(map(int, f.read().strip().split()))

    stones = Counter(data)
    blinks = 75
    for _ in range(blinks):
        new_stones = defaultdict(int)
        # print(f'computing blink {i+1}')
        for stone, count in stones.items():
            for output_stone in eval_stone(stone):
                new_stones[output_stone] += count
        stones = new_stones
    
    total = sum(stones.values())
    print(f'{total = }')


main()