from pathlib import Path

from problem import AOCProblem, Direction2D, Coordinate2D


class TodaysProblem(AOCProblem):
    N = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movements = []
        self.head = Coordinate2D()
        self.tail = Coordinate2D()
        self._tail_histo = {self.tail}

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                segments = line.split()
                self.movements.append((Direction2D[segments[0]], int(segments[1])))

    def solve1(self):
        for direction, amount in self.movements:
            for _ in range(amount):
                self.head += direction
                self._make_tail_follow_head()

        return len(self._tail_histo)


    def solve2(self):
        pass

    def _make_tail_follow_head(self):
        if self.head.chess_king_distance(self.tail) <= 1:
            return

        diff = self.head - self.tail

        diff_1_step = diff.to_king_move()
        new_tail = self.tail + diff_1_step

        self.tail = new_tail
        self._tail_histo.add(new_tail)

    def _plot(self):
        y0 = min(self.head.y, self.tail.y, 0)
        yf = max(self.head.y, self.tail.y, 0)
        x0 = min(self.head.x, self.tail.x, 0)
        xf = max(self.head.x, self.tail.x, 0)

        for y in range(y0, yf+1):
            for x in range(x0, xf+1):
                if (y, x) == self.head and self.head == self.tail:
                    c = 'X'
                elif (y, x) == self.head:
                    c = 'H'
                elif (y, x) == self.tail:
                    c = 'T'
                elif not x and not y:
                    c = 'S'
                else:
                    c = '.'

                print(c, end='')

            print()

    def __str__(self):
        return '\n'.join((' '.join(str(x) for x in row) for row in self.movements))


if __name__ == '__main__':
    TodaysProblem(test=False)()
