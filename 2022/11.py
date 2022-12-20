from pathlib import Path

from problem import AOCProblem


class TodaysProblem(AOCProblem):
    N = 11

    MONKEYS = []

    class Monkey:
        def __init__(self, n):
            self.n = n

            self.items = []
            self.mod = -1
            self.operation = None
            self.true_monkey = -1
            self.false_monkey = -1

        def __str__(self):
            return f'{self.n}: {self.items} M=[{self.mod}]; T->{self.true_monkey} F->{self.false_monkey}'

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
                    last_monkey.items.extend(list(map(int, value.split(','))))
                    continue

                if 'Test' in field:
                    last_monkey.mod = int(value.strip().split(' ')[-1])
                    continue

                if 'Operation' in field:
                    last_monkey.operation = lambda x: eval(f'old={x};{value};print(new)')  # FIXME
                    continue

                if 'true' in field:
                    last_monkey.true_monkey = int(value.strip().split(' ')[-1])
                    continue
                if 'false' in field:
                    last_monkey.false_monkey = int(value.strip().split(' ')[-1])
                    continue

    def solve1(self):

        print(*self.MONKEYS, sep='\n')

    def solve2(self):
        pass

    def __str__(self):
        return '\n'.join(str(m) for m in self.MONKEYS)


if __name__ == '__main__':
    TodaysProblem(test=True)()
