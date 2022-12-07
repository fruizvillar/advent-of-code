from enum import Enum
from io import StringIO
from pathlib import Path

N = 3

TEST = False

IN = Path('in') / f'{N:02d}.txt'

IN_TEST = StringIO(
    '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw''')

def calc_priority(c):
    return ord(c) - (ord('a') if c.islower() else ord('A') - 26) + 1


def solve():
    buffer = IN_TEST if TEST else IN.open()

    with buffer as f:
        backpacks = [line.strip() for line in f.readlines()]

    sum_priorities = 0

    for backpack in backpacks:
        n_items = len(backpack)
        pocket1 = set(backpack[:n_items//2])
        pocket2 = set(backpack[n_items//2:])

        extra_item = pocket1.intersection(pocket2).pop()  # type: str

        sum_priorities += calc_priority(extra_item)

    print('First star result:', sum_priorities)

    # 2nd star
    sum_groups = 0

    items_in_group = set()

    for i, backpack in enumerate(backpacks):

        if i % 3 == 0:
            if items_in_group:
                sum_groups += calc_priority(items_in_group.pop())

            items_in_group = set(backpack)

        else:
            items_in_group = items_in_group.intersection(set(backpack))

    if items_in_group:
        sum_groups += calc_priority(items_in_group.pop())

    print('Second star result:', sum_groups)


if __name__ == '__main__':
    solve()
