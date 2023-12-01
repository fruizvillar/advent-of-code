from enum import StrEnum, auto
from pathlib import Path

from lib import AOCProblem


class Problem(AOCProblem):
    N = 10

    class Instruction(StrEnum):
        NOOP = auto()
        ADDX = auto()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instructions = []
        self.x = 1
        self._sum_mul_20 = 0
        self._ctr_row = []
        self._ctr_rows = []

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                parts = line.split()
                self.instructions.append((self.Instruction(parts[0]),) + tuple(int(x) for x in parts[1:]))

    def solve1(self):

        cycle = 0

        for instruction_extra in self.instructions:
            cycle += 1
            instruction = instruction_extra[0]
            extras = instruction_extra[1:]

            self._p(cycle)

            if instruction == self.Instruction.ADDX:
                cycle += 1
                self._p(cycle)

                self.x += extras[0]

        return self._sum_mul_20

    def _p(self, cycle):
        s = cycle * self.x

        if cycle % 20 == 0 and cycle % 40 == 20:
            self._sum_mul_20 += s

    def solve2(self):
        self.x = 1
        cycle = 0

        for instruction_extra in self.instructions:
            cycle += 1
            instruction = instruction_extra[0]
            extras = instruction_extra[1:]

            self._pc(cycle)

            if instruction == self.Instruction.ADDX:
                cycle += 1
                self._pc(cycle)

                self.x += extras[0]

        return '\n' + '\n'.join(self._ctr_rows)

    def _pc(self, cycle):
        if abs(self.x - ((cycle - 1) % 40)) <= 1:
            cp = '#'
        else:
            cp = '.'
        self._ctr_row.append(cp)

        if cycle % 40 == 0:
            self._ctr_rows.append(''.join(self._ctr_row))
            self._ctr_row = []

    def __str__(self):
        return '\n'.join((' '.join(str(x) for x in row) for row in self.instructions))


if __name__ == '__main__':
    Problem(test=False)()
