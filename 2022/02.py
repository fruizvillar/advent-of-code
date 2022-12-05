import heapq
from pathlib import Path

N = 2

IN = Path('in') / f'{N:02d}.txt'

oponent_opts = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
}
my_opts = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors',
}

value_my = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}

with IN.open() as f:

    score = 0

    n = -1
    for line in f.readlines():
        n+=1
        line = line.strip()
        oponent_c, mine_c = line.split(' ')

        oponent = oponent_opts[oponent_c]
        mine = my_opts[mine_c]

        score += value_my[mine]

        wdl = 0
        if mine == oponent:
            wdl = 3

        elif mine == 'scissors':
            if oponent == 'paper':
                wdl = 6

        elif mine == 'paper':
            if oponent == 'stone':
                wdl = 6
        else:
            if oponent == 'scissors':
                wdl = 6

        score += wdl + value_my[mine]
        print(f'{n:4}. {oponent_c} {oponent:8} v. {mine_c} {mine:8} =  {wdl}+{value_my[mine]}')

print(score)
