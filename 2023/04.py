import dataclasses
import re

import lib


@dataclasses.dataclass
class ScratchCard:
    id: int
    winning: set
    mine: set
    union: set = dataclasses.field(default_factory=set)
    amount: int = 1


class Problem(lib.AOCProblem):
    """2023/04 puzzle https://adventofcode.com/2023/day/4"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)

        self.cards = {}

    def load_data(self, f):
        with f.open() as f_in:
            for i, line in enumerate(f_in):
                info = line.strip().split(':')[1].strip()
                winning_str, mine_str = info.split('|')

                winning = set(int(x) for x in winning_str.strip().split(' ') if x)
                mine = set(int(x) for x in mine_str.strip().split(' ') if x)

                self.cards[i] = ScratchCard(i, winning, mine)

    def _fill_union(self):
        for card in self.cards.values():
            card.union = card.winning & card.mine

    def solve1(self):
        self._fill_union()

        points = 0

        for card in self.cards.values():

            if card.union:
                points += 2 ** (len(card.union) - 1)

        return points

    def solve2(self):

        for i, card in self.cards.items():
            for j in range(len(card.union)):
                self.cards[i + j + 1].amount += card.amount

        return sum(card.amount for card in self.cards.values())


if __name__ == '__main__':
    Problem()()
