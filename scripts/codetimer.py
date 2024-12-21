import re
import sys
import time


def time_script(script: str, ignore_prints: bool = False):
    t0 = time.perf_counter_ns()
    d = {}
    code = open(script).read()
    if ignore_prints:
        code = re.sub(r'print\(.+\)', 'pass', code)
    exec(code, d, d)
    t1 = time.perf_counter_ns()
    return (t1 - t0) / 1e6

if __name__ == '__main__':
    script = sys.argv[1]
    t = time_script(script)
    print(f'execution completed in {t:0.3f} ms')
