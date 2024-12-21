import os
import pathlib

from codetimer import time_script


def get_aoc_scripts():
    paths = []
    items = os.listdir('.')
    for folder in items:
        if not folder.startswith('day'):
            continue
        filenames = os.listdir(folder)
        for filename in filenames:
            if not filename.endswith('.py'):
                continue
            path = pathlib.Path(folder, filename)
            paths.append(str(path))
    return paths

def main():
    scripts = get_aoc_scripts()
    for script in scripts:
        t = time_script(script, ignore_prints=True)
        print(f'{script:<15} | {t:>9.3f} ms')


if __name__ == '__main__':
    main()