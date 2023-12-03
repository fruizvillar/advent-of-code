import dataclasses
import re

import lib


@dataclasses.dataclass
class Number:
    n: int
    y: int
    x0: int
    xf: int
    part: bool = False


@dataclasses.dataclass
class Symbol:
    s: str
    y: int
    x: int
    numbers: list = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Gear:
    n0: int
    n1: int

    @property
    def ratio(self):
        return self.n0 * self.n1


RE_NUMBER = re.compile(r'(\d+)')

RE_SYMBOL = re.compile(r'([^.\n0-9])')


class Problem(lib.AOCProblem):
    """2023/03 puzzle https://adventofcode.com/2023/day/3"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)
        self.numbers = []
        self.symbols = []
        self.gears = []

    def load_data(self, f):
        with f.open() as f_in:

            for i, line in enumerate(f_in.readlines()):
                for match in RE_NUMBER.finditer(line):
                    self.numbers.append(Number(int(match.groups()[0]), i, match.start(0), match.end(0)))

                for match in RE_SYMBOL.finditer(line):
                    self.symbols.append(Symbol(match.groups()[0], i, match.start(0)))

    def _connect_numbers_with_symbols(self):
        for n in self.numbers:
            for s in self.symbols:
                if abs(s.y - n.y) <= 1 and n.x0 - 1 <= s.x < n.xf + 1:
                    n.part = True
                    s.numbers.append(n.n)

    def _load_gears(self):
        for s in self.symbols:
            if s.s != '*':
                continue

            if len(numbers := s.numbers) != 2:
                continue
            self.gears.append(Gear(*numbers))

    def solve1(self):
        self._connect_numbers_with_symbols()

        return sum(n.n for n in self.numbers if n.part)

    def solve2(self):
        self._load_gears()
        return sum(g.ratio for g in self.gears)


if __name__ == '__main__':
    Problem()()
