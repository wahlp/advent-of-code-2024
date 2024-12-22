def parse_input(filename):
    with open(f'day22/{filename}') as f:
        data = f.read().splitlines()
    return [int(x) for x in data]

def mix_and_prune(value, secret):
    secret = value ^ secret
    secret = secret % 16777216
    return secret

def process(secret):
    secret = mix_and_prune(secret * 64, secret)
    secret = mix_and_prune(secret // 32, secret)
    secret = mix_and_prune(secret * 2048, secret)
    return secret

def solve(num, steps):
    for _ in range(steps):
        num = process(num)
    return num

def main(filename):
    data = parse_input(filename)
    return sum(solve(n, 2000) for n in data)


assert main('sample.txt') == 37327623
r = main('input.txt')
print(r)