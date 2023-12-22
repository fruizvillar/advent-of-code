import enum

import lib


class Problem(lib.AOCProblem):
    """2023-12-14 puzzle https://adventofcode.com/2023/day/14"""

    class Symbols(enum.StrEnum):
        ROUNDED_ROCK = 'O'
        CUBE_SHAPED_ROCK = '#'
        EMPTY = '.'

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self.grid = lib.AOCGrid(types=self.Symbols)

        self.cube_shaped_rocks = []
        self.rounded_rocks = []

    def load_data(self, f):
        self.grid.load_f(f)

    def solve1(self):
        self._load_rocks()

        self.calc_pos_tilt(direction=lib.Direction2D.U)
        return self._weight()

    def solve2(self, n=1_000_000_000):
        self._load_rocks()  # We are actually resetting them

        grids = {}
        weights = {}

        cycle_0 = cycle_f = None

        for i in range(n):

            if (se := self.hash()) in grids:
                cycle_0 = grids[se]
                cycle_f = i
                self.logger.debug(f'Cycle detected @ {i} SE: {se}')
                self.logger.debug(f'Cycle length {cycle_f - cycle_0}, cycle offset {cycle_0}')

                break

            grids[se] = i
            weights[i] = self._weight()

            self.logger.debug(f'Cycle {i} weight {weights[i]:3}. SE: {se}')

            self._cycle()

        if cycle_0 is None:
            return weights[n - 1]

        equivalent_n = cycle_0 + (n - cycle_f) % (cycle_f - cycle_0)
        self.logger.debug(f'Equivalent n: {equivalent_n}')
        return weights[equivalent_n]

    def _cycle(self):
        for tilt_direction in (lib.Direction2D.U, lib.Direction2D.L, lib.Direction2D.D, lib.Direction2D.R):
            self.calc_pos_tilt(tilt_direction)

    def calc_pos_tilt(self, direction: lib.Direction2D):

        iter_axis = self.grid.Axis.ROW if direction in (lib.Direction2D.U, lib.Direction2D.D) else self.grid.Axis.COL
        iter_reverse = direction in (lib.Direction2D.D, lib.Direction2D.R)

        for pos, item in self.iter_rounded_rocks(axis=iter_axis, reverse=iter_reverse):
            new_pos = self._recurse_tilt(pos, direction)

            self.move_rock(pos, new_pos)

    def _recurse_tilt(self, pos, tilt_direction):

        if (next_pos := pos + tilt_direction) in self.cube_shaped_rocks:
            return pos

        if self.grid.pos_is_oob(next_pos):
            return pos

        if next_pos in self.rounded_rocks:
            return pos

        return self._recurse_tilt(next_pos, tilt_direction)

    def _load_rocks(self):
        cube_rocks = []
        rounded_rocks = []

        for position, item in self.grid.iter_with_pos():
            if item == self.Symbols.CUBE_SHAPED_ROCK:
                cube_rocks.append(position)
                continue

            if item == self.Symbols.ROUNDED_ROCK:
                rounded_rocks.append(position)

        self.cube_shaped_rocks = cube_rocks
        self.rounded_rocks = rounded_rocks

    def move_rock(self, rock: lib.Position2D, to: lib.Position2D):
        if rock == to:
            return

        self.rounded_rocks.remove(rock)
        self.rounded_rocks.append(to)

    def iter_rounded_rocks(self, axis: lib.AOCGrid.Axis, reverse=False):
        for pos in sorted(self.rounded_rocks, key=lambda p: p.as_tuple()[axis.value], reverse=reverse):
            yield pos, self.grid[pos]

    def _weight(self):
        weight = 0

        for pos in self.rounded_rocks:
            weight += self.grid.height - pos.y

        return weight

    def print(self):
        print(str(self).replace('|', '\n'), end='\n\n')

    def __str__(self):
        rows = []

        for y in range(self.grid.height):

            row = []
            for x in range(self.grid.width):
                if (y, x) in self.rounded_rocks:
                    row.append(self.Symbols.ROUNDED_ROCK)
                elif (y, x) in self.cube_shaped_rocks:
                    row.append(self.Symbols.CUBE_SHAPED_ROCK)
                else:
                    row.append(self.Symbols.EMPTY)

            rows.append(''.join(row))

        return '|'.join(rows)

    def hash(self):
        return '|'.join(f'RR({p.y},{p.x})' for p in self.rounded_rocks)


if __name__ == '__main__':
    Problem()()
