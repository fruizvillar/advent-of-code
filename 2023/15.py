import dataclasses

import lib


class Problem(lib.AOCProblem):
    """2023-12-15 puzzle https://adventofcode.com/2023/day/15"""

    @dataclasses.dataclass
    class Lens:
        name: str
        focal_length: int = dataclasses.field(default=-1, compare=False)

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self.check = None
        self.check_values = []
        self.boxes: dict[int, list[Problem.Lens]] = {n: [] for n in range(256)}

    def load_data(self, f):
        with f.open() as f_in:
            self.check_values = f_in.readline().split(',')

    def solve1(self):
        t = 0
        for v in self.check_values:
            h = self._hash(v)
            t += h

        return t

    def solve2(self):
        for item in self.check_values:
            self.logger.debug(f'Processing {item}')
            self._process(item)
            self.print()

        return self.focusing_power()

    def _process(self, item):
        if '=' in item:
            return self._add(item)

        if item.endswith('-'):
            return self._remove(item)

        raise RuntimeError(f'Unknown item {item}')

    def _add(self, item):
        item_name, focal_length = item.split('=')
        focal_length = int(focal_length)
        box = self._hash(item_name)
        lens = self.Lens(item_name, focal_length)

        try:
            lens_idx = self.boxes[box].index(lens)
        except ValueError:
            lens_idx = None

        if lens_idx is not None:
            self.boxes[box][lens_idx].focal_length = focal_length
            self.logger.debug(f'Updated {lens}')
            return

        self.boxes[box].append(self.Lens(item_name, focal_length))

    def _remove(self, item):
        item_name = item[:-1]
        box = self._hash(item_name)

        try:
            self.boxes[box].remove(self.Lens(item_name))
        except ValueError:
            self.logger.debug(f'Nothing to remove for {item}')

    @staticmethod
    def _hash(string):
        result = 0
        for c in string:
            result += ord(c)
            result *= 17
            result %= 256

        return result

    def focusing_power(self, boxes=None):
        boxes = boxes or self.boxes

        result = 0
        for n_box, box in boxes.items():
            for n_slot, slot in enumerate(box, start=1):
                result += (n_box + 1) * n_slot * slot.focal_length

        return result

    def print(self):
        for n_box, box in self.boxes.items():
            if not box:
                continue
            self.logger.debug(f'Box {n_box}: {box}')

    def test_it(self):
        assert self.focusing_power({0: [self.Lens('rn', 1)]}) == 1
        assert self.focusing_power({3: [self.Lens('ot', 7)]}) == 28


if __name__ == '__main__':
    instance = Problem()
    instance.test_it()
    instance()
