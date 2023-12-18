import collections
import enum

import lib


class Problem(lib.AOCProblem):
    """2023-12-13 puzzle https://adventofcode.com/2023/day/13"""

    class Symbols(enum.StrEnum):
        ASH = '.'
        ROCKS = '#'

    _PRINT_MAP = {
        Symbols.ASH: '▢',
        Symbols.ROCKS: '▣',

    }

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)

        self.grids: list[lib.AOCGrid] = []
        self.repeated = set()

    def load_data(self, f):
        with open(f) as f_in:
            rows = f_in.readlines()

        last_read = 0
        for i in range(len(rows)):

            if rows[i].strip():
                continue

            self.grids.append(lib.AOCGrid(rows=rows[last_read:i], types=self.Symbols))
            last_read = i + 1

        self.grids.append(lib.AOCGrid(rows=rows[last_read:], types=self.Symbols))

    def solve1(self):
        acc = 0
        for grid in self.grids:
            mc = self._mirror_cols(grid) or [0]
            mr = self._mirror_rows(grid) or [0]
            acc += mc[0] + 100 * mr[0]

        return acc

    def solve2(self):
        acc = 0

        for grid_n, grid in enumerate(self.grids):
            part_1_col = self._mirror_cols(grid)
            part_1_row = self._mirror_rows(grid)

            acc_xy = 0

            it = 0
            for y in range(grid.height):
                reflexion_found = False
                for x in range(grid.width):
                    new_grid = grid.copy()
                    new_grid[y, x] = self.Symbols.ROCKS if grid[y, x] == self.Symbols.ASH else self.Symbols.ASH

                    new_row_val = set(self._mirror_rows(new_grid))
                    new_row_val = list(new_row_val - set(part_1_row))
                    new_col_val = []

                    if not new_row_val:
                        new_col_val = set(self._mirror_cols(new_grid))
                        new_col_val = list(new_col_val - set(part_1_col))

                        if not new_col_val:
                            it += 1
                            continue

                    new_row_val = new_row_val or [0]
                    new_col_val = new_col_val or [0]
                    acc_xy = 100 * new_row_val[0] + new_col_val[0]

                    reflexion_found = True
                    break

                if reflexion_found:
                    break

            if not acc_xy:
                raise RuntimeError('No reflexion found')
            acc += acc_xy

        return acc

    def _mirror_cols(self, grid, ) -> list[int]:
        return self._find_mirror_edge(grid.cols, grid.width, )

    def _mirror_rows(self, grid, ) -> list[int]:
        return self._find_mirror_edge(grid.rows, grid.height, )

    @staticmethod
    def _find_mirror_edge(iterator: list[list[Symbols]], it_len) -> list[int]:

        same_sequences = collections.defaultdict(list)
        for i, sequence in enumerate(iterator):
            same_sequences[tuple(sequence)].append(i)

        sharing_seq_0 = [idx for idx in same_sequences.values() if 0 in idx][0]
        sharing_seq_f = [idx for idx in same_sequences.values() if it_len - 1 in idx][0]

        mirror_positions = []
        if sharing_seq_0:
            for idx_reflection in sharing_seq_0:
                if idx_reflection % 2 == 0:
                    # A mirror needs to be in the middle of two sequences.
                    continue

                mirror_pos = 1 + idx_reflection // 2

                reflects = True
                for idx in range(1, mirror_pos):
                    if iterator[idx] != iterator[idx_reflection - idx]:
                        reflects = False
                        break

                if not reflects:
                    continue

                mirror_positions.append(mirror_pos)

        if sharing_seq_f:
            for idx_reflection in sharing_seq_f:
                if (idx_reflection + it_len) % 2 != 0:
                    # A mirror needs to be in the middle of two sequences.
                    continue

                mirror_pos = (idx_reflection + it_len) // 2

                reflects = True
                for idx in range(1, it_len - mirror_pos):
                    if iterator[mirror_pos - idx] != iterator[mirror_pos + idx - 1]:
                        reflects = False
                        break

                if not reflects:
                    continue

                mirror_positions.append(mirror_pos)

        return mirror_positions

    def _print_info(self, i, grid, new_grid, *args):
        print(
            f'Trying {i:2d}|', ''.join(self._c(x) for x in grid[0]), '|', ''.join(self._c(x) for x in new_grid[0]),
            '|', *args)
        for i in range(1, grid.height):
            print(
                '         |', ''.join(self._c(x) for x in grid[i]), '|', ''.join(self._c(x) for x in new_grid[i]),
                '|')

        print()

    def _c(self, s):
        return self._PRINT_MAP[s]


if __name__ == '__main__':
    Problem()()
