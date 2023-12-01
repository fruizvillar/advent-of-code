import heapq

from lib import AOCProblem


class Day01(AOCProblem):
    N = 1

    def solve1(self, buffer):
        return self._solve(buffer, 1)

    def solve2(self, buffer):
        return self._solve(buffer, 3)

    def _solve(self, buffer, n):
        h = []

        ei = 0

        for raw in buffer.readlines():

            if line := raw.strip():
                ei += int(line)

            else:
                heapq.heappush(h, ei)
                ei = 0

        return sum(heapq.nlargest(n, h))


if __name__ == '__main__':
    Day01()()
