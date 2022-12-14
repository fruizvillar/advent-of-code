from pathlib import Path

from problem import AOCProblem


class TodaysProblem(AOCProblem):
    N = 8

    MAX_TREE_H = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.forest = []
        self.h = self.w = 0
        self.visible_trees = set()

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                self.forest.append(list(map(int, line.strip())))

        self.h = len(self.forest)
        self.w = len(self.forest[0])

    def solve1(self):
        edge_trees = 2 * (self.h + self.w - 2)

        # Up to down
        visible_trees = self._vertical_sweep()

        # Down to up
        visible_trees |= self._vertical_sweep(revert=True)

        # L to R
        visible_trees |= self._horizontal_sweep()

        # R to L
        visible_trees |= self._horizontal_sweep(revert=True)

        self.visible_trees = visible_trees

        return len(visible_trees) + edge_trees

    def solve2(self):
        max_score = 0
        for y0, x0 in self.visible_trees:
            if x0 in (0, self.w - 1) or y0 in (0, self.h - 1):
                continue

            product = []
            for dy, dx in (0, 1), (1, 0), (-1, 0), (0, -1):
                pass

    def _vertical_sweep(self, revert=False):
        visible_trees = set()

        first_col = (self.h - 1) if revert else 0

        highest_tree = {row: self.forest[row][first_col] for row in range(1, self.h - 1)}

        range_sweep_col = range(1, self.h - 1)
        if revert:
            range_sweep_col = reversed(range_sweep_col)

        for col in range_sweep_col:
            done_with_row = []
            for row, highest in highest_tree.items():
                if (tree_h := self.forest[row][col]) > highest:
                    highest_tree[row] = tree_h
                    visible_trees.add((row, col))

                if max(highest, tree_h) == self.MAX_TREE_H:
                    done_with_row.append(row)

            for row in done_with_row:
                del highest_tree[row]

            if not highest_tree:
                break

        return visible_trees

    def _horizontal_sweep(self, revert=False):
        visible_trees = set()

        first_row = (self.h - 1) if revert else 0

        highest_tree = {i: self.forest[first_row][i] for i in range(1, self.w - 1)}

        range_sweep_row = range(1, self.h - 1)
        if revert:
            range_sweep_row = reversed(range_sweep_row)

        for row in range_sweep_row:
            done_with_col = []
            for col, highest in highest_tree.items():
                if (tree_h := self.forest[row][col]) > highest:
                    highest_tree[col] = tree_h
                    visible_trees.add((row, col))

                if max(highest, tree_h) == self.MAX_TREE_H:
                    done_with_col.append(col)

            for col in done_with_col:
                del highest_tree[col]

            if not highest_tree:
                break

        return visible_trees

    def __str__(self):
        return '\n'.join((''.join(str(x) for x in row) for row in self.forest))


if __name__ == '__main__':
    TodaysProblem(test=False)()
