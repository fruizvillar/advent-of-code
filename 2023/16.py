import enum
import queue

import lib


class Problem(lib.AOCProblem):
    """2023-12-16 puzzle https://adventofcode.com/2023/day/16"""

    class Symbols(enum.StrEnum):
        MIRROR_RU = '/'
        MIRROR_LU = '\\'
        SPLITTER_UD = '|'
        SPLITTER_LR = '-'
        EMPTY = '.'

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self.grid = lib.AOCGrid(types=self.Symbols)

    def load_data(self, f):
        self.grid.load_f(f)

    def solve1(self):
        self.grid.print()

        return self._get_energized_positions(init_pos=lib.Position2D(0, 0), init_d=lib.Direction2D.R)

    def _get_energized_positions(self, init_pos, init_d):
        process_queue = queue.Queue()
        process_queue.put((init_pos, init_d))

        energized_positions = set()
        history = set()

        while not process_queue.empty():
            pos, direction = process_queue.get()
            if (pos, direction) in history:
                self.logger.debug(f'Already processed {pos} {direction}')
                continue
            history.add((pos, direction))

            self.logger.debug(f'Processing {pos} {direction}')
            if self.grid.pos_is_oob(pos):
                continue

            energized_positions.add(pos)
            new_directions = []

            match symbol := self.grid[pos]:
                case self.Symbols.MIRROR_LU:
                    new_directions = [self._swap_direction(direction, (lib.Direction2D.U, lib.Direction2D.L))]

                case self.Symbols.MIRROR_RU:
                    new_directions = [self._swap_direction(direction, (lib.Direction2D.U, lib.Direction2D.R))]
                case self.Symbols.SPLITTER_UD:
                    new_directions = self._split_direction(direction, (lib.Direction2D.U, lib.Direction2D.D))
                case self.Symbols.SPLITTER_LR:
                    new_directions = self._split_direction(direction, (lib.Direction2D.L, lib.Direction2D.R))
                case self.Symbols.EMPTY:
                    new_directions = [direction]

            for d in new_directions:
                new_pos = pos + d
                if self.grid.pos_is_oob(new_pos):
                    continue
                self.logger.debug(f'Processing {pos} ({symbol}) to new direction {d}')
                process_queue.put((new_pos, d))

        return len(energized_positions)

    def solve2(self):
        max_energy = 0
        for y in range(self.grid.height):
            energy_0 = self._get_energized_positions(init_pos=lib.Position2D(y, x=0), init_d=lib.Direction2D.R)

            xf = self.grid.width - 1
            energy_f = self._get_energized_positions(init_pos=lib.Position2D(y, x=xf), init_d=lib.Direction2D.L)
            max_energy = max(max_energy, energy_0, energy_f)

        for x in range(self.grid.width):
            energy_0 = self._get_energized_positions(init_pos=lib.Position2D(y=0, x=x), init_d=lib.Direction2D.D)

            yf = self.grid.height - 1
            energy_f = self._get_energized_positions(init_pos=lib.Position2D(y=yf, x=x), init_d=lib.Direction2D.U)
            max_energy = max(max_energy, energy_0, energy_f)



        return max_energy
    def _swap_direction(self, direction, directions):
        directions_a = set(directions)
        directions_b = set(lib.Direction2D) - directions_a
        if direction in directions_a:
            for d in directions_a:
                if d != direction:
                    return d

        if direction in directions_b:
            for d in directions_b:
                if d != direction:
                    return d

        raise ValueError(f'Invalid direction {direction}')

    def _split_direction(self, direction, directions):
        if direction in directions:
            return [direction]

        return directions


if __name__ == '__main__':
    Problem(verbose=False)()
