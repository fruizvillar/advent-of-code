import enum
import itertools

import lib


class Problem(lib.AOCProblem):
    """2023-12-11 puzzle https://adventofcode.com/2023/day/11"""

    class SpaceItems(enum.StrEnum):
        VACUUM = '.'
        GALAXY = '#'

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)

        self.galaxies = set()
        self.empty_rows = []
        self.empty_cols = []
        self.expansions = []

    def load_data(self, f):

        occupied_cols = set()
        with f.open() as f_in:
            for y, line in enumerate(f_in):

                if self.SpaceItems.GALAXY not in line:
                    self.empty_rows.append(y)
                    continue

                for x, c in enumerate(line):
                    if c == self.SpaceItems.GALAXY:
                        self.galaxies.add(lib.Position2D(y, x))
                        occupied_cols.add(x)

        self.empty_cols = [c for c in range(max(occupied_cols)) if c not in occupied_cols]

    def solve1(self):
        return self._solve()

    def solve2(self):
        return self._solve(factor=1_000_000)

    def _solve(self, factor=1):
        shortest_paths_sum = 0
        for g1, g2 in itertools.combinations(sorted(self.galaxies), 2):
            d = g1.manhattan_distance(g2)

            expansion_effect = self._expansion_between(g1, g2, factor)
            self.expansions.append((g1, g2, factor, expansion_effect))
            shortest_paths_sum += d + expansion_effect
            self.logger.debug('Distance %s <-> %s = %d. (exp=%d)', g1, g2, d, expansion_effect)

        return shortest_paths_sum

    def _expansion_between(self, g1, g2, expansion_factor=2):
        exp_y = exp_x = 0

        if g1.y != g2.y:
            min_g_y = min(g1.y, g2.y)
            max_g_y = max(g1.y, g2.y)
            exp_y = sum(1 for y in range(min_g_y + 1, max_g_y) if y in self.empty_rows)

        if g1.x != g2.x:
            min_g_x = min(g1.x, g2.x)
            max_g_x = max(g1.x, g2.x)
            exp_x = sum(1 for x in range(min_g_x + 1, max_g_x) if x in self.empty_cols)

        return (expansion_factor - 1) * (exp_y + exp_x)


if __name__ == '__main__':
    Problem(test=False)()
