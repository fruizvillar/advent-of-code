import dataclasses
import re

import lib


@dataclasses.dataclass
class Play:
    red: int = 0
    blue: int = 0
    green: int = 0

    def __post_init__(self):
        self.red = int(self.red)
        self.blue = int(self.blue)
        self.green = int(self.green)

    @property
    def power(self):
        return self.red * self.blue * self.green


_COLOURS = ['red', 'blue', 'green']

RE = {c: re.compile(fr'(\d+) {c}') for c in _COLOURS}


class Problem(lib.AOCProblem):
    """2023/02 puzzle https://adventofcode.com/2023/day/2"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)
        self.games = {}

    def load_data(self, f):
        with f.open() as f_in:
            for i, line in enumerate(f_in.readlines()):
                plays = []
                for play in line.split(':')[1].split(';'):
                    play_dict = {}
                    for c in _COLOURS:
                        if match := RE[c].search(play):
                            play_dict[c] = match.groups()[0]

                    plays.append(Play(**play_dict))

                self.games[i + 1] = plays

    def solve1(self):

        max_cubes = Play(12, 13, 14)

        count = 0

        for i, game in self.games.items():
            valid_game = True

            for play in game:
                if play.red > max_cubes.red or play.green > max_cubes.green or play.blue > max_cubes.blue:
                    valid_game = False
                    break

            if valid_game:
                count += i

        return count

    def solve2(self):
        power_sum = 0
        for i, game in self.games.items():

            min_cubes_for_game = Play()

            for play in game:
                if play.red > min_cubes_for_game.red:
                    min_cubes_for_game.red = play.red
                if play.green > min_cubes_for_game.green:
                    min_cubes_for_game.green = play.green
                if play.blue > min_cubes_for_game.blue:
                    min_cubes_for_game.blue = play.blue

            power_sum += min_cubes_for_game.power
        return power_sum


if __name__ == '__main__':
    Problem()()
