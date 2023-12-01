import math
from enum import Enum
from itertools import product, tee
from pathlib import Path

from lib import AOCProblem


class Problem(AOCProblem):
    N = 8

    MAX_TREE_H = 9

    class Direction(Enum):
        H = 'horizontal'
        V = 'vertical'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.forest = []
        self.dim = 0
        self.visible_trees = set()

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                self.forest.append(list(map(int, line.strip())))

        self.dim = len(self.forest)

    def solve1(self):
        edge_trees = 4 * (self.dim - 1)

        visible_trees = set()

        for direction, reverting in product(self.Direction, (False, True)):
            visible_trees |= self.sweep_forest(direction, reverting)

        self.visible_trees = visible_trees

        return len(visible_trees) + edge_trees

    def solve2(self):
        max_score = 0

        for y0, x0 in product(*tee(range(1, self.dim - 1))):

            factors = []

            for dy, dx in (-1, 0), (0, -1), (1, 0), (0, 1):
                y, x = y0, x0
                n_trees = 0
                this_tree_h = self.forest[y][x]
                while x and y:
                    y, x = y + dy, x + dx

                    try:
                        next_tree_h = self.forest[y][x]
                    except IndexError:
                        break

                    n_trees += 1

                    if next_tree_h >= this_tree_h:
                        break

                factors.append(n_trees)

            max_score = max(max_score, math.prod(factors))

        return max_score

    def sweep_forest(self, sweep_dir: Direction, revert=False):
        visible_trees = set()

        first_n_along_sweep = (self.dim - 1) if revert else 0

        if sweep_dir == self.Direction.V:
            highest_tree_per_across_line = {i: self.forest[first_n_along_sweep][i] for i in range(1, self.dim - 1)}
        else:
            highest_tree_per_across_line = {i: self.forest[i][first_n_along_sweep] for i in range(1, self.dim - 1)}

        range_sweep = range(1, self.dim - 1)
        if revert:
            range_sweep = reversed(range_sweep)

        # n_along is the index along (parallel to) the direction in which we sweep (sweep=H -> n_along=n_row)
        for n_along in range_sweep:
            done_with_n_across = []
            for n_across, highest in highest_tree_per_across_line.items():

                row, col = (n_along, n_across) if sweep_dir == self.Direction.V else (n_across, n_along)

                if (tree_h := self.forest[row][col]) > highest:
                    highest_tree_per_across_line[n_across] = tree_h
                    visible_trees.add((row, col))

                if max(highest, tree_h) == self.MAX_TREE_H:
                    done_with_n_across.append(n_across)

            for n_across in done_with_n_across:
                del highest_tree_per_across_line[n_across]

            if not highest_tree_per_across_line:
                break

        return visible_trees

    def __str__(self):
        return '\n'.join((''.join(str(x) for x in row) for row in self.forest))


if __name__ == '__main__':
    Problem(test=False)()
