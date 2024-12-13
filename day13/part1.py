import re

PATTERN = r"""
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
""".strip()

BUTTON_A_COST = 3
BUTTON_B_COST = 1
MAX_PRESSES_PER_BUTTON = 100

def eval_machine(segment):
    match = re.match(PATTERN, segment)
    (
        button_a_x, 
        button_a_y, 
        button_b_x, 
        button_b_y,
        prize_x, 
        prize_y 
    ) = list(map(int, match.groups()))

    for b_presses in range(MAX_PRESSES_PER_BUTTON + 1):
        for a_presses in range(MAX_PRESSES_PER_BUTTON + 1):
            destination = (
                b_presses * button_b_x + a_presses * button_a_x,
                b_presses * button_b_y + a_presses * button_a_y,
            )
            if destination == (prize_x, prize_y):
                answer = a_presses * BUTTON_A_COST + b_presses * BUTTON_B_COST
                return answer
    return 0


def main():
    with open('day13/input.txt') as f:
        data = f.read().split('\n\n')

    total = 0
    for segment in data:
        total += eval_machine(segment)
    print(f'{total = }')

main()
