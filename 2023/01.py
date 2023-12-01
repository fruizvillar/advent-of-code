import pathlib
import re

import lib


class TodaysProblem(lib.AOCProblem):
    """ https://adventofcode.com/2023/day/1

    Solved by matching digits in the string, and then converting them to ints. Mapping is done from digit names to
    ints, and the last digit is found by reversing the string and matching again."""

    _DIGITS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    _RE_D = '|'.join(_DIGITS.keys())
    _RE_D_REVERSED = '|'.join("".join(reversed(key)) for key in _DIGITS.keys())

    RE_DIGITS = re.compile(r'(\d)')

    RE = re.compile(fr'(\d|{_RE_D})')
    RE_REVERSED = re.compile(fr'(\d|{_RE_D_REVERSED})')

    def __init__(self, test: bool = False):
        super().__init__(dunder_file_child=__file__, test=test)
        self.data = None

    def load_data(self, f: pathlib.Path):
        with f.open() as fd:
            self.data = fd.read()

    def solve1(self):
        return self._solve(digits_only=True)

    def solve2(self):
        return self._solve(digits_only=False)

    def _solve(self, *, digits_only):
        acc = 0
        for s in self.data.splitlines():
            matches = self._match(s, digits_only)
            n = matches[0] * 10 + matches[-1]

            acc += n

        return acc

    def _match(self, s, digits_only):
        pos = 0

        pattern = self.RE_DIGITS if digits_only else self.RE

        first_match = pattern.search(s, pos).group(0)
        last_match = self._last_match(s, digits_only)

        matches = [first_match, last_match]
        matches = [int(self._DIGITS.get(m, m)) for m in matches]

        return matches

    def _last_match(self, s, digits_only):
        if digits_only:
            return self.RE_DIGITS.findall(s)[-1]

        else:
            s_reversed = ''.join(reversed(s))
            matched_str = self.RE_REVERSED.search(s_reversed).group(0)
            return ''.join(reversed(matched_str))


if __name__ == '__main__':
    TodaysProblem()()
