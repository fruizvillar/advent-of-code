import lib


class Problem(lib.AOCProblem):
    """YYYY-12-DD puzzle https://adventofcode.com/YYYY/day/D"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)

    def load_data(self, f):
        with f.open() as f_in:
            pass

    def solve1(self):
        pass

    def solve2(self):
        pass


if __name__ == '__main__':
    Problem(test=True)()
