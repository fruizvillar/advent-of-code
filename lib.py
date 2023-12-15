import abc
import dataclasses
import enum
import logging
import math
import typing
from pathlib import Path


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


class _Base2D:

    def __init__(self, y, x=None):
        if x is None:
            if isinstance(y, tuple):
                self._tuple = y
            elif isinstance(y, _Base2D):
                self._tuple = y.as_tuple()
            else:
                raise ValueError(f'What is {y=}?')
        else:
            self._tuple = (y, x)

    @property
    def y(self):
        return self._tuple[0]

    @property
    def x(self):
        return self._tuple[1]

    def as_tuple(self) -> tuple:
        return self._tuple

    def __neg__(self) -> '_Base2D':
        return self.__class__((-self.y, -self.x))

    def __eq__(self, other):
        if isinstance(other, _Base2D):
            other = other.as_tuple()
        elif hasattr(other, 'pos'):
            other = other.pos.as_tuple()
        if not isinstance(other, tuple):
            raise NotImplementedError

        return self._tuple == other

    def __str__(self):
        return f'({self.y: d}, {self.x: d})'

    def __hash__(self):
        return self._tuple.__hash__()

    def __lt__(self, other):
        return self._tuple.__lt__(other.as_tuple())


class Position2D(_Base2D):

    def iter_direction_neighbours(self, include_diagonals=False, filter_out_of_bounds=False, use_coordinates=False):
        min_y = min_x = - math.inf
        max_y = max_x = math.inf

        if filter_out_of_bounds:
            min_y = min_x = 0
            if isinstance(filter_out_of_bounds, bool):
                pass  # otherwise it matches int!
            elif isinstance(filter_out_of_bounds, int):
                max_y = filter_out_of_bounds - 1
                max_x = filter_out_of_bounds -1
            elif isinstance(filter_out_of_bounds, tuple) and len(filter_out_of_bounds) == 2:
                max_y, max_x = [c - 1 for c in filter_out_of_bounds]

        neighbours_direction = list(Coordinate) if use_coordinates else list(Direction2D)
        if include_diagonals:
            neighbours_direction.extend(CoordinateDiagonals if use_coordinates else DirectionDiagonals2D)

        for direction in neighbours_direction:
            new_coord = self + direction
            if not (min_y <= new_coord.y <= max_y):
                continue
            if not (min_x <= new_coord.x <= max_x):
                continue

            yield direction, new_coord

    def chess_king_distance(self, other):
        other = _Base2D(other)
        diff = self - other

        return max(abs(diff.y), abs(diff.x))  # Diagonal moves would make the lower component irrelevant

    def manhattan_distance(self, other):
        other = _Base2D(other)
        diff = self - other

        return abs(diff.y) + abs(diff.x)

    def to_king_move(self) -> '_Base2D':

        return _Base2D(*[c // abs(c) if c else 0 for c in self._tuple])

    def __add__(self, other) -> '_Base2D':
        if isinstance(other, _Base2D):
            return self.__class__(self.y + other.y, self.x + other.x)

        if isinstance(other, tuple) and len(other) == 2:
            return self.__class__(self.y + other[0], self.x + other[1])

        raise NotImplementedError

    def __sub__(self, other) -> '_Base2D':
        return self.__add__(other.__neg__())

    def __str__(self):
        return f'P({self.y: d}, {self.x: d})'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.y}, {self.x})'


class _BaseEnum2D(_Base2D, tuple, enum.Enum):
    def __init__(self, y, x=None):
        super().__init__(y, x)
        if isinstance(y, tuple):
            self._tuple = y
        else:
            self._tuple = (y, x)


class Coordinate2D(_BaseEnum2D):
    """Indicates any direction in a 2D grid (unitary vector). Format N-S-W-E"""
    N = (-1, +0)
    S = (+1, +0)
    W = (+0, -1)
    E = (+0, +1)


Coordinate = Coordinate2D


class CoordinateDiagonals(_BaseEnum2D):
    """Indicates any coordinates in a 2D grid (unitary vector)"""
    NW = (-1, -1)
    NE = (-1, +1)
    SW = (+1, -1)
    SE = (+1, +1)


class Direction2D(_BaseEnum2D):
    """Indicates any direction in a 2D grid (unitary vector). Format U-D-L-R"""
    U = (-1, +0)
    D = (+1, +0)
    L = (+0, -1)
    R = (+0, +1)


class DirectionDiagonals2D(_BaseEnum2D):
    """Indicates any direction in a 2D grid (unitary vector)"""
    UL = (-1, -1)
    UR = (-1, -1)
    DL = (+1, -1)
    DR = (+1, -1)


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
