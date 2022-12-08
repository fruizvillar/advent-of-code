import dataclasses
import queue
import re
from io import StringIO
from pathlib import Path

N = 6

TEST = False

IN = Path('in') / f'{N:02d}.txt'
IN.touch()

IN_TEST = StringIO('''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw''')


def find_idx_n_distinct_chars(word, n):
    idx = 0
    last_n_c = []
    while True:
        last_n_c.append(word[idx])

        if len(last_n_c) > n:
            last_n_c = last_n_c[1:]

        idx += 1

        if len(last_n_c) == len(set(last_n_c)) == n:
            break

    return idx


def solve():
    buffer = IN_TEST if TEST else IN.open()

    messages = []

    with buffer as f:
        messages.extend(line.strip() for line in f.readlines())

    for message in messages:

        idx = find_idx_n_distinct_chars(message, 4)

        print('First star result:', idx)

    for message in messages:

        idx = find_idx_n_distinct_chars(message, 14)

        print('Second star result:', idx)

if __name__ == '__main__':
    solve()
