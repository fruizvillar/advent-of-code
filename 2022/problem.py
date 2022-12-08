import abc
from io import StringIO
from pathlib import Path


class AOCProblem(abc.ABC):

    N = None

    def __init__(self, test_input=None):

        self.input_f = Path('in') / f'{self.N:02d}.txt'

        self.test_input = test_input

    def solve1(self, buffer):
        raise NotImplementedError

    def solve2(self, buffer):
        raise NotImplementedError

    def __call__(self, test=False):
        test_str = ' (test)' if test else ''

        buffer_f = StringIO(self.test_input) if test else self.input_f.open()

        with buffer_f as buffer:
            result = self.solve1(buffer)
        print(f'First star result{test_str}:', result)

        buffer_f = StringIO(self.test_input) if test else self.input_f.open()

        with buffer_f as buffer:
            result = self.solve2(buffer)
        print(f'Second star result{test_str}:', result)





