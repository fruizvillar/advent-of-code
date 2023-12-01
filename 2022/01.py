import heapq

from lib import AOCProblem


class Problem(AOCProblem):
    N = 1

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)
        self.lines = []

    def load_data(self, f):
        with f.open() as f_in:
            self.lines = f_in.readlines()

    def solve1(self):
        return self._solve(n_largest=1)

    def solve2(self):
        return self._solve(n_largest=3)

    def _solve(self, n_largest):
        heap = []

        ei = 0

        for line_raw in self.lines:

            if line := line_raw.strip():
                ei += int(line)

            else:
                heapq.heappush(heap, ei)
                ei = 0

        return sum(heapq.nlargest(n_largest, heap))


if __name__ == '__main__':
    Problem()()
