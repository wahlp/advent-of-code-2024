from common import get_aoc_scripts


def measure_size(script):
    code = open(script).read()
    size = len(code)

    comments = 0
    for line in code.splitlines():
        if line.strip().startswith('#'):
            comments += 1
    
    return size, comments
    

def main():
    scripts = get_aoc_scripts()
    
    print(f'{'script':<15} | {'size':>6} | {'comments':>9}')
    print(f'{'-'.ljust(15, '-')}-+-{'-'.rjust(6, '-')}-+-{'-'.rjust(9, '-')}')
    for script in scripts:
        size, comments = measure_size(script)
        print(f'{script:<15} | {size:>6} | {comments:>9}')


if __name__ == '__main__':
    main()
