import abc
import dataclasses
import logging
from enum import Enum
from pathlib import Path
from typing import Literal


@dataclasses.dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length - 1

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __post_init__(self):
        if self.length < 1:
            raise RuntimeError('Range length must be positive')

    def overlapping(self, other: 'Range'):

        if other.start in self:
            first_range = self
            second_range = other
        elif self.start in other:
            first_range = other
            second_range = self
        else:
            return None

        return Range(second_range.start, min(first_range.end, second_range.end) - second_range.start + 1)


class Direction2D(Enum):
    """Indicates any direction in a 2D grid (unitary vector)"""
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)

    @property
    def y(self) -> Literal[-1, 0, 1]:
        """ Y coordinate of the direction"""
        return self.value[0]

    @property
    def x(self) -> Literal[-1, 0, 1]:
        """ X coordinate of the direction"""
        return self.value[1]


class Coordinate2D:

    def __init__(self, y=0, x=0):

        if isinstance(y, (Coordinate2D, Direction2D)):
            self.y = y.y
            self.x = y.x
            return

        if isinstance(y, tuple):
            self.y, self.x = y
            return

        self.y = y
        self.x = x

    @property
    def as_tuple(self) -> tuple:
        return self.y, self.x

    def __add__(self, other) -> 'Coordinate2D':
        if isinstance(other, (Coordinate2D, Direction2D)):
            return Coordinate2D(self.y + other.y, self.x + other.x)

        if isinstance(other, tuple) and len(other) == 2:
            return Coordinate2D(self.y + other[0], self.x + other[1])

        raise NotImplementedError

    def __neg__(self) -> 'Coordinate2D':
        return Coordinate2D(-self.y, -self.x)

    def __sub__(self, other) -> 'Coordinate2D':
        return self.__add__(other.__neg__())

    def __eq__(self, other):
        if isinstance(other, Coordinate2D):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple):
            return self.as_tuple == other

    def __str__(self):
        return f'({self.y: d}, {self.x: d})'

    def chess_king_distance(self, other):
        other = Coordinate2D(other)

        abs_y = abs(self.y - other.y)
        abs_x = abs(self.x - other.x)

        return max(abs_y, abs_x)  # Diagonal moves would make the lower component irrelevant

    def to_king_move(self) -> 'Coordinate2D':
        mod_y = self.y // abs(self.y) if self.y else 0
        mod_x = self.x // abs(self.x) if self.x else 0
        return Coordinate2D(mod_y, mod_x)

    def __hash__(self):
        return self.as_tuple.__hash__()

    def __lt__(self, other):
        return self.as_tuple.__lt__(other.as_tuple)


class AOCProblem(abc.ABC):

    def __init__(self, dunder_file_child, test=False, verbose=False):
        caller_f = Path(dunder_file_child)

        self.day = int(caller_f.stem)
        self.year = int(caller_f.parent.name)

        input_f_stem = caller_f.parent.parent / 'in' / f'{self.year:02d}' / f'{self.day:02d}'
        self.input_f = input_f_stem.with_suffix('.txt')
        self.input_f_test = input_f_stem.with_suffix('.test.txt')
        self.test = test

        if not (f_applicable := self.input_f_test if test else self.input_f).exists():
            if not (parent := f_applicable.parent).exists():
                parent.mkdir(parents=True)
                print('Just created the input folder:', parent.as_uri())

            f_applicable.touch()
            print(f'Just created {f_applicable.as_uri()}. Paste your input there!')
            raise SystemExit(1)

        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        self.logger = logging.getLogger(f'advent-of-code_{self.year}-{self.day:02d}')

    def load_data(self, f: Path):
        raise NotImplementedError

    def solve1(self):
        raise NotImplementedError

    def solve2(self):
        raise NotImplementedError

    def __call__(self):
        test_str = ' (test)' if self.test else ''

        f = self.input_f_test if self.test else self.input_f

        print(f'Solving AoC day {self.day}{test_str}. See https://adventofcode.com/{self.year}/day/{self.day}.')

        self.load_data(f)

        result = self.solve1()
        print(f'First star result{test_str}:', result)

        result = self.solve2()
        print(f'Second star result{test_str}:', result)
