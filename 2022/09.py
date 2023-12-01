from pathlib import Path

from lib import AOCProblem, Direction2D, Coordinate2D


class Problem(AOCProblem):
    N = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movements = []
        self._knots = []
        self._tail_histo = {Coordinate2D()}

    @property
    def head(self):
        return self._knots[0]

    @property
    def tail(self):
        return self._knots[-1]

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                segments = line.split()
                self.movements.append((Direction2D[segments[0]], int(segments[1])))

    def solve1(self):
        return self._solve()

    def solve2(self):
        return self._solve(n_knots=10)

    def _solve(self, n_knots=2):
        self._knots = [Coordinate2D()] * n_knots
        self._tail_histo = {self.tail}

        for direction, amount in self.movements:
            for _ in range(amount):
                self._knots[0] += direction
                self._make_tail_follow_head()

        self._plot()

        return len(self._tail_histo)

    def _make_tail_follow_head(self):

        for n in range(1, len(self._knots)):
            if self._knots[n - 1].chess_king_distance(self._knots[n]) <= 1:
                return

            diff = self._knots[n - 1] - self._knots[n]

            diff_1_step = diff.to_king_move()
            self._knots[n] += diff_1_step

        self._tail_histo.add(self.tail)

    def _plot(self):
        y0 = min(0, *[c.y for c in self._knots], *[c.y for c in self._tail_histo])
        yf = max(0, *[c.y for c in self._knots], *[c.y for c in self._tail_histo])
        x0 = min(0, *[c.x for c in self._knots], *[c.x for c in self._tail_histo])
        xf = max(0, *[c.x for c in self._knots], *[c.x for c in self._tail_histo])

        print('-' * (xf - x0 + 1))
        for y in range(y0, yf + 1):
            for x in range(x0, xf + 1):
                c = self._find_c(y, x)
                print(c, end='')

            print()

    def _find_c(self, y, x):
        p = Coordinate2D(y, x)

        for i, knot in enumerate(self._knots):
            if p == knot:
                if i == 0:
                    return 'H'
                return str(i)

        if p in self._tail_histo:
            return '#'

        if y or x:
            return '.'
        return 's'

    def __str__(self):
        return '\n'.join((' '.join(str(x) for x in row) for row in self.movements))


if __name__ == '__main__':
    Problem(test=False)()
