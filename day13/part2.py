import re

PATTERN = r"""
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
""".strip()

OFFSET = 10000000000000

def eval_machine(segment):
    match = re.match(PATTERN, segment)
    (
        ax, 
        ay, 
        bx, 
        by,
        cx, 
        cy 
    ) = list(map(int, match.groups()))

    cx += OFFSET
    cy += OFFSET

    #       a * ax + b * bx = cx      (1)
    #       a * ay + b * by = cy      (2)
    #
    # using (1) * ay
    #       ay * (a * ax + b * bx) = ay * cx
    # multiply a
    #       a * (ax * ay) + b * (bx * ay) = ay * cx       (4)
    #
    # using (2) * ax
    #       ax * (a * ay + b * by) = ax * cy
    # multiply a
    #       a * (ay * ax) + b * (by * ax) = ax * cy       (3)
    #
    # subtract (4) from (3) 
    #       (a * (ax * ay) + b * (bx * ay)) - (a * (ay * ax) + b * (by * ax)) = (ay * cx) - (ax * cy)
    # cancel out 'a' terms
    #       b * (bx * ay - by * ax) = ay * cx - ax * cy
    # make b the left hand side of the eq
    b = (ax * cy - ay * cx) / (ax * by - ay * bx)
    # rearrange (1)
    a = (cx - bx * b) / ax

    if a.is_integer() and b.is_integer():
        return int(a * 3 + b)
    return 0


def main():
    with open('day13/input.txt') as f:
        data = f.read().split('\n\n')

    total = 0
    for segment in data:
        total += eval_machine(segment)
    print(f'{total = }')

main()

