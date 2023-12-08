import lib


class Problem(lib.AOCProblem):
    """2023/06 puzzle https://adventofcode.com/2023/day/6"""

    ACC = 1

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)

        self.times = []
        self.distances = []

    def load_data(self, f):
        with f.open() as f_in:
            for line in f_in:
                line = line.strip()
                if not line:
                    continue

                if 'Time:' in line:
                    self.times.extend([int(n) for n in line.split(':')[1].split(' ') if n])

                elif 'Distance:' in line:
                    self.distances.extend([int(n) for n in line.split(':')[1].split(' ') if n])

    def solve1(self):
        print(self.times)
        print(self.distances)

        results = 1

        for round_no, (time_avail, distance_thr) in enumerate(zip(self.times, self.distances)):
            n_working = self._solve_race(round_no, distance_thr, time_avail)

            results *= n_working

        return results

    def solve2(self):
        round_no = 1

        time_avail = int(''.join(str(n) for n in self.times))
        distance_thr = int(''.join(str(n) for n in self.distances))

        return self._solve_race(round_no, distance_thr, time_avail)

    def _solve_race(self, round_no, distance_thr, time_avail):
        print(f'Round {round_no + 1}: {time_avail = } ms, {distance_thr = } mm')
        n_working = 0
        for time_pressed in range(1, time_avail):
            speed = time_pressed * self.ACC
            time_travelling = time_avail - time_pressed
            distance_travelled = time_travelling * speed

            if distance_travelled <= distance_thr:
                if n_working:
                    break
                else:
                    continue

            # print(f'  {time_pressed = } ms -> {speed =} mm/ms, {time_travelling = } ms, {distance_travelled = } mm')
            n_working += 1
        return n_working


if __name__ == '__main__':
    Problem(test=False)()
