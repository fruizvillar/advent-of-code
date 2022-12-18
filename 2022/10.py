import math
from enum import Enum, StrEnum, auto
from itertools import product, tee
from pathlib import Path
from typing import Set, Tuple

from problem import AOCProblem


class TodaysProblem(AOCProblem):
    N = 10

    class Instruction(StrEnum):
        NOOP = auto()
        ADDX = auto()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instructions = []
        self.x = 1

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                parts = line.split()
                self.instructions.append((self.Instruction(parts[0]),) + tuple(parts[1:]))

    def solve1(self):

        for instruction_extra in self.instructions:
            instruction = instruction_extra[0]
            extras = instruction_extra[1:]
            print(instruction, extras)


    def solve2(self):
        pass
    def __str__(self):
        return '\n'.join((' '.join(str(x) for x in row) for row in self.instructions))


if __name__ == '__main__':
    TodaysProblem(test=True)()
