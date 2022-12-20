import abc
from pathlib import Path

class AOCProblem(abc.ABC):
    N = None

    def __init__(self, test=False):
        self.input_f = (Path('in') / f'{self.N:02d}.txt').resolve()
        self.input_f_test = self.input_f.with_name(f'{self.N:02d}_test.txt')
        self.test = test

        f_applicable = self.input_f_test if test else self.input_f

        if not f_applicable.exists():
            f_applicable.touch()
            print(f'Just created {f_applicable.as_uri()}. Paste your input there!')
            raise RuntimeError

    def load_data(self, f: Path):
        raise NotImplementedError

    def solve1(self):
        raise NotImplementedError

    def solve2(self):
        raise NotImplementedError

    def __call__(self):
        test_str = ' (test)' if self.test else ''

        f = self.input_f_test if self.test else self.input_f

        print(f'Solving AoC day {self.N}{test_str}. See https://adventofcode.com/2022/day/{self.N}.')

        self.load_data(f)

        result = self.solve1()
        print(f'First star result{test_str}:', result)

        result = self.solve2()
        print(f'Second star result{test_str}:', result)
