import dataclasses
from io import StringIO
from pathlib import Path

N = 4

TEST = False

IN = Path('in') / f'{N:02d}.txt'
IN.touch()

IN_TEST = StringIO(
    '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8''')


@dataclasses.dataclass
class Interval:
    left: int
    right: int

    def contains(self, other: 'Interval') -> bool:
        if self.left <= other.left and self.right >= other.right:
            return True
        return False

    def overlaps(self, other: 'Interval') -> bool:
        if self.right >= other.left >= self.left:
            return True
        if self.right >= other.right >= self.left:
            return True
        if other.contains(self):
            return True
        return False

    def __str__(self):
        return f'I({self.left:2d}, {self.right:2d})'


def solve():
    buffer = IN_TEST if TEST else IN.open()

    intervals = []
    with buffer as f:
        for line in f.readlines():
            for interval_str in line.strip().split(','):
                intervals.append(Interval(*(int(x) for x in interval_str.split('-'))))

    count_subintervals = count_overlapping = 0

    for couple_idx in range(len(intervals) // 2):
        i = couple_idx * 2
        j = i + 1

        interval1 = intervals[i]
        interval2 = intervals[j]

        if interval1.contains(interval2) or interval2.contains(interval1):
            count_subintervals += 1
            count_overlapping += 1

        elif interval1.overlaps(interval2):
            count_overlapping += 1

    print('First star result:', count_subintervals)
    print('Second star result:', count_overlapping )


if __name__ == '__main__':
    solve()
