from collections import defaultdict


def parse_input(filename):
    with open(f'day22/{filename}') as f:
        data = f.read().splitlines()
    return [int(x) for x in data]

def process(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

def simulate_prices(num: int, steps: int):
    prices = []
    price_changes = []
    for i in range(steps):
        prices.append(num % 10)
        if i > 0:
            price_changes.append(prices[-1] - prices[-2])
        num = process(num)
    return prices, price_changes

def solve(prices_data):
    all_profit = defaultdict(int)
    for prices, price_changes in prices_data:
        expected_profit: dict[tuple[int, ...], int] = {}
        for i in range(len(price_changes) - 4):
            changes = tuple(price_changes[i:i + 4])
            profit = prices[i + 4]
            if changes not in expected_profit:
                expected_profit[changes] = profit
        for pattern, profit in expected_profit.items():
            all_profit[pattern] += profit
    # best_pattern = max(all_profit, key=all_profit.get)
    return max(all_profit.values())

def main(filename: str):
    data = parse_input(filename)
    prices_data = [simulate_prices(n, 2000) for n in data]
    r = solve(prices_data)
    return r


assert main('sample2.txt') == 23
r = main('input.txt')
print(r)