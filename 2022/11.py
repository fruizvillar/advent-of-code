from pathlib import Path
from queue import SimpleQueue
from typing import List

from lib import AOCProblem


class Problem(AOCProblem):
    N = 11

    N_ROUNDS = 20

    class Monkey:
        def __init__(self, n):
            self.n = n

            self.items = SimpleQueue()
            self.mod = -1
            self.equation = None
            self.true_monkey = -1
            self.false_monkey = -1
            self.n_inspections = 0

        def operation(self, old):
            self.n_inspections += 1
            return eval(self.equation)

        def __str__(self):
            return f'{self.n}: Q({str(self.items):20}) [%{self.mod}]; T->{self.true_monkey} F->{self.false_monkey}'

    MONKEYS: List[Monkey] = []

    def load_data(self, f: Path):
        n_monkeys = 0
        last_monkey = None

        with f.open() as buffer:
            for line in buffer.readlines():
                if not line.strip():
                    continue

                fields = line.split(':')

                field, value = fields

                if 'Monkey' in fields[0]:
                    last_monkey = self.Monkey(n_monkeys)
                    self.MONKEYS.append(last_monkey)
                    n_monkeys += 1

                    continue

                if 'Starting items' in field:
                    for item in map(int, value.split(',')):
                        last_monkey.items.put_nowait(item)
                    continue

                if 'Test' in field:
                    last_monkey.mod = int(value.strip().split(' ')[-1])
                    continue

                if 'Operation' in field:
                    last_monkey.equation = value.split('=')[1]
                    continue

                if 'true' in field:
                    last_monkey.true_monkey = int(value.strip().split(' ')[-1])
                    continue
                if 'false' in field:
                    last_monkey.false_monkey = int(value.strip().split(' ')[-1])
                    continue

    def solve1(self):
        return self._solve(div=3, n_rounds=20)

    def solve2(self):
        print('Cannot solve with brute-force methods!')
        return
        self._solve(div=1, n_rounds=10000)

    def _solve(self, div, n_rounds):
        for n_round in range(1, n_rounds + 1):

            for monkey in self.MONKEYS:

                while not monkey.items.empty():
                    item = monkey.items.get_nowait()
                    worry_level = monkey.operation(item) // div

                    if worry_level % monkey.mod == 0:
                        passing_to_m = monkey.true_monkey
                    else:
                        passing_to_m = monkey.false_monkey

                    self.MONKEYS[passing_to_m].items.put_nowait(worry_level)

            print(f'At the end of round {n_round}:')

            print('N Inspections', *(f'{m.n}: {m.n_inspections}' for m in self.MONKEYS), sep='\n\t')

        inspections = sorted(m.n_inspections for m in self.MONKEYS)
        return inspections[-1] * inspections[-2]

    def __str__(self):
        return '\n'.join(str(m) for m in self.MONKEYS)


if __name__ == '__main__':
    Problem(test=True)()
