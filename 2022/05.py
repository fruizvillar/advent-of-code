import dataclasses
import queue
import re
from io import StringIO
from pathlib import Path

N = 5

TEST = False

IN = Path('in') / f'{N:02d}.txt'
IN.touch()

IN_TEST = StringIO('''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2''')


@dataclasses.dataclass
class Movement:
    amount: int
    origin: int
    destination: int


regex_move = re.compile(r'move (\d+) from (\d+) to (\d+)')

def solve():
    buffer = IN_TEST if TEST else IN.open()

    piles_str = []
    movements = []
    with buffer as f:
        while line := f.readline().replace('\n', ''):
            piles_str.append(line)
        while line := f.readline().strip():
            movements.append(Movement(*(int(x) for x in regex_move.match(line).groups())))

    n_piles = [int(p_n) for p_n in piles_str[-1].split() if p_n]

    piles = {n: queue.LifoQueue() for n in n_piles}

    for level in piles_str[-2::-1]:
        for p_n in piles.keys():
            if c := level[1+(p_n-1)*4].strip():
                piles[p_n].put_nowait(c)

    for m in movements:
        for _ in range(m.amount):
            c = piles[m.origin].get_nowait()
            piles[m.destination].put_nowait(c)

    word = ''.join(q.get_nowait() for q in piles.values())

    print('First star result:', word)

    piles = {n: queue.LifoQueue() for n in n_piles}

    for level in piles_str[-2::-1]:
        for p_n in piles.keys():
            if c := level[1+(p_n-1)*4].strip():
                piles[p_n].put_nowait(c)

    aux_q = queue.LifoQueue()
    for m in movements:

        for _ in range(m.amount):
            c = piles[m.origin].get_nowait()
            aux_q.put_nowait(c)

        for _ in range(m.amount):
            c = aux_q.get_nowait()
            piles[m.destination].put_nowait(c)

    word = ''.join(q.get_nowait() for q in piles.values())
    print('Second star result:', word)


if __name__ == '__main__':
    solve()
