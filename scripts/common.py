import os
import pathlib


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