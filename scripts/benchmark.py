import sys
from enum import Enum

from codetimer import time_script
from common import get_aoc_scripts


class SortBy(Enum):
    name = 0
    runtime = 1

def main(sort_by: SortBy = SortBy.name):
    scripts = get_aoc_scripts()
    data = [(script, time_script(script, ignore_prints=True)) for script in scripts]
    data.sort(key=lambda x: x[sort_by.value])

    print(f'{'script':<15} | {'time':>9}')
    print(f'{'-'.ljust(15, '-')}-+-{'-'.rjust(9, '-')}')
    for script, runtime in data:
        print(f'{script:<15} | {runtime:>9.3f} ms')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sort_by = SortBy[sys.argv[1]]
        main(sort_by)
    else:
        main()