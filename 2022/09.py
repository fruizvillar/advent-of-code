from pathlib import Path

from problem import AOCProblem, Direction2D


class TodaysProblem(AOCProblem):
    N = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movements = []

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                segments = line.split()
                self.movements.append((Direction2D[segments[0]], segments[1]))

    def solve1(self):
        print(self)

    def solve2(self):
        pass

    def __str__(self):
        return '\n'.join((' '.join(str(x) for x in row) for row in self.movements))


if __name__ == '__main__':
    TodaysProblem(test=False)()
