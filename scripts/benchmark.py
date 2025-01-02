import sys
from enum import Enum

from codetimer import time_script
from common import get_aoc_scripts


class SortBy(Enum):
    name = 0
    runtime = 1

def main(sort_by: SortBy = SortBy.name):
    scripts = get_aoc_scripts()
    
    data = []
    for script in scripts:
        print(f'running script: {script}', end='\r')
        t = time_script(script, ignore_prints=True)
        data.append((script, t))

    data.sort(key=lambda x: x[sort_by.value])

    print(f'{'script':<15} | {'time':>9}')
    print(f'{'-'.ljust(15, '-')}-+-{'-'.rjust(9, '-')}')
    for script, runtime in data:
        print(f'{script:<15} | {runtime:>9.3f} ms')
    total_runtime = sum(t for _, t in data)
    print(f'\n{'total':<15} | {total_runtime:>9.3f} ms')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sort_by = SortBy[sys.argv[1]]
        main(sort_by)
    else:
        main()