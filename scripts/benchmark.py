from codetimer import time_script
from common import get_aoc_scripts


def main():
    scripts = get_aoc_scripts()
    for script in scripts:
        t = time_script(script, ignore_prints=True)
        print(f'{script:<15} | {t:>9.3f} ms')


if __name__ == '__main__':
    main()