from enum import Enum
from io import StringIO
from pathlib import Path

N = 2

TEST = False

IN = Path('in') / f'{N:02d}.txt'

IN_TEST = StringIO('A Y\nB X\nC Z')


class WhatToDo(Enum):
    LOSE = 'X'
    DRAW = 'Y'
    WIN = 'Z'


class RPC(Enum):
    ROCK = ('A', 'X', 1)
    PAPER = 'B', 'Y', 2
    SCISSORS = 'C', 'Z', 3

    @classmethod
    def from_opponent_choice(cls, choice) -> 'RPC':
        return [option for option in list(cls) if option.value[0] == choice][0]

    @classmethod
    def from_my_choice(cls, choice) -> 'RPC':
        return [option for option in list(cls) if option.value[1] == choice][0]

    @property
    def score(self) -> int:
        return self.value[-1]


def rate_score(opponent: RPC, mine: RPC):
    if mine == opponent:
        wdl = 3

    elif ((mine == RPC.SCISSORS and opponent == RPC.PAPER) or
          (mine == RPC.PAPER and opponent == RPC.ROCK) or
          (mine == RPC.ROCK and opponent == RPC.SCISSORS)):
        wdl = 6
    else:
        wdl = 0

    return wdl + mine.score


def solve():
    buffer = IN_TEST if TEST else IN.open()

    with buffer as f:
        plays = [line.strip().split(' ') for line in f.readlines()]

    score = n = 0
    for opponent_c, mine_c in plays:
        opponent = RPC.from_opponent_choice(opponent_c)
        mine = RPC.from_my_choice(mine_c)

        round_score = rate_score(opponent, mine)
        score += round_score

        print(f'{n:4}. {opponent:8} v. {mine:8} =  {round_score}')
        n += 1

    print('First star result:', score)

    score = n = 0
    for opponent_c, what_to_do_c in plays:
        opponent = RPC.from_opponent_choice(opponent_c)
        what_to_do = WhatToDo(what_to_do_c)

        mine = None

        if what_to_do == WhatToDo.DRAW:
            mine = opponent

        elif what_to_do == WhatToDo.WIN:
            if opponent == RPC.ROCK:
                mine = RPC.PAPER
            elif opponent == RPC.PAPER:
                mine = RPC.SCISSORS
            elif opponent == RPC.SCISSORS:
                mine = RPC.ROCK
        elif what_to_do == WhatToDo.LOSE:
            if opponent == RPC.ROCK:
                mine = RPC.SCISSORS
            elif opponent == RPC.PAPER:
                mine = RPC.ROCK
            elif opponent == RPC.SCISSORS:
                mine = RPC.PAPER

        if mine is None:
            raise RuntimeError('Algo Problem!')

        round_score = rate_score(opponent, mine)
        score += round_score

        print(f'{n:4}. ({what_to_do}) {opponent:8} v. {mine:8} =  {round_score}')
        n += 1

    print('Second star result:', score)


if __name__ == '__main__':
    solve()
