import sys
from enum import Enum

from common import get_aoc_scripts


def measure_size(script):
    code = open(script).read()
    size = len(code)

    comments = 0
    for line in code.splitlines():
        if line.strip().startswith('#'):
            comments += 1
    
    return size, comments


class SortBy(Enum):
    name = 0
    size = 1
    comments = 2


def main(sort_by: SortBy = SortBy.name):
    scripts = get_aoc_scripts()
    data = [(script, *measure_size(script)) for script in scripts]
    data.sort(key=lambda x: x[sort_by.value])
    
    print(f'{'script':<15} | {'size':>6} | {'comments':>9}')
    print(f'{'-'.ljust(15, '-')}-+-{'-'.rjust(6, '-')}-+-{'-'.rjust(9, '-')}')
    for script, size, comments in data:
        print(f'{script:<15} | {size:>6} | {comments:>9}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sort_by = SortBy[sys.argv[1]]
        main(sort_by)
    else:
        main()
