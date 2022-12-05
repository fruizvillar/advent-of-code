import heapq
from pathlib import Path

N = 1

IN = Path('in') / f'{N:02d}.txt'

h = []

ei = 0

N_ELVES = 3


with IN.open() as f:
    for raw in f.readlines():

        if line := raw.strip():
            ei += int(line)

        else:
            heapq.heappush(h, ei)
            ei = 0

print(sum(heapq.nlargest(3, h)))

