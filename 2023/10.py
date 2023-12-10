import lib


class Problem(lib.AOCProblem):
    """2023-12-10 puzzle https://adventofcode.com/2023/day/10"""

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)

    def load_data(self, f):
        with f.open() as f_in:
            pass

    def solve1(self):
        pass

    def solve2(self):
        pass


if __name__ == '__main__':
    Problem(test=True, verbose=True)()
