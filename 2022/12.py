from pathlib import Path
from typing import List, Optional

from lib import AOCProblem, Coordinate2D


class TodaysProblem(AOCProblem):
    N = 12

    C_START = 'S'
    C_END = 'E'

    _START_END = [None, None]  # type: List[Optional[Coordinate2D]]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.riverside = []

    def load_data(self, f: Path):

        with f.open() as buffer:
            for (y, line) in enumerate(buffer.readlines()):
                self.riverside.append(list(line.strip()))

                for start_end_pos, c in zip((0, 1), (self.C_START, self.C_END)):

                    try:
                        x = line.index(c)
                    except ValueError:
                        continue

                    self._START_END[start_end_pos] = Coordinate2D(y, x)

    def solve1(self):
        return self._solve()

    def solve2(self):
        return self._solve()

    def _solve(self):
        print(*self.riverside, sep='\n')
        print(self.start, self.end)

    @property
    def start(self):
        return self._START_END[0]

    @property
    def end(self):
        return self._START_END[1]


if __name__ == '__main__':
    TodaysProblem(test=True)()
