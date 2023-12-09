import lib

import collections


class Problem(lib.AOCProblem):
    """YYYY-12-09 puzzle https://adventofcode.com/YYYY/day/9"""

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self.histories = []

    def load_data(self, f):
        with f.open() as f_in:
            for line in f_in:
                self.histories.append(tuple(map(int, line.split(' '))))

    def solve1(self):
        print(self.histories)

        return sum(self._forecast(history) for history in self.histories)

    def solve2(self):
        return sum(self._forecast(history, backwards=True) for history in self.histories)

    def _forecast(self, history, backwards=False):

        last_value_idx = 0 if backwards else -1

        hist_matrix = self._hist_matrix(history)

        last_value = None
        new_last_value = None

        for hist in reversed(hist_matrix):
            if last_value is None:
                new_last_value = 0

            else:
                if backwards:
                    new_last_value = hist[last_value_idx] - last_value
                else:
                    new_last_value = hist[last_value_idx] + last_value

            # We add to different ends of the deque depending on the direction
            if backwards:
                hist.appendleft(new_last_value)
            else:
                hist.append(new_last_value)

            last_value = new_last_value

        self._print_hist_matrix(hist_matrix)

        return new_last_value

    def _hist_matrix(self, history) -> list[collections.deque]:
        hist_matrix = [collections.deque(history)]

        while any(last_hist := hist_matrix[-1]):
            hist_matrix.append(collections.deque(last_hist[x + 1] - last_hist[x] for x in range(len(last_hist) - 1)))

        self._print_hist_matrix(hist_matrix)

        return hist_matrix

    def _print_hist_matrix(self, hist_matrix):
        self.logger.debug(f'hist_matrix:')
        for n, hist in enumerate(hist_matrix):
            str_hist = ' | '.join(map(lambda x: f'{x:3}', hist))
            self.logger.debug(f'{" " * 2 * n}{str_hist}')


if __name__ == '__main__':
    Problem()()
