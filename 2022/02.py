import heapq
from pathlib import Path

N = 2

IN = Path('in') / f'{N:02d}.txt'

oponent_opts = {
    'rock': 'A',
    'paper': 'B',
    'scissors': 'C',
}
my_opts = {
    'rock': 'X',
    'paper': 'Y',
    'scissors': 'Z',
}

with IN.open() as f:

    score = 0

    for line in f.readlines():
        line = line.strip()
        oponent, mine = line.split(' ')



print(sum(heapq.nlargest(3, h)))

