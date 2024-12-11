def eval_stone(value: int):
    if value == 0:
        return [1]
    
    v = str(value)
    if len(v) % 2 == 0:
        mid = len(v) // 2
        return [int(v[:mid]), int(v[mid:])]
    
    return [value * 2024]
    
def main():
    with open('day11/input.txt') as f:
        data = list(map(int, f.read().strip().split()))

    blinks = 25
    for _ in range(blinks):
        new_data = []
        for stone in data:
            new_data.extend(eval_stone(stone))
        data = new_data
    
    print(len(data))


main()