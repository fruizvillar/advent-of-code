import dataclasses
import enum
import queue
import re

import lib


class SpringCondition(enum.StrEnum):
    """Status of the spring"""
    OPERATIONAL = '.'
    DAMAGED = '#'
    UNKNOWN = '?'


_RE_DAMAGED_SPRING = re.compile(r'\.*([#?]+)')


class Problem(lib.AOCProblem):
    """2023-12-12 puzzle https://adventofcode.com/2023/day/12"""

    @dataclasses.dataclass
    class SpringRow:

        record: str
        groups: list
        n_options: int = 0

        def __post_init__(self):
            self.n_options = self._get_n_options()

        def _get_n_options(self):
            n_options = 0

            record_queue = queue.LifoQueue()

            record_queue.put(self.record)

            while not record_queue.empty():
                record = record_queue.get()
                # print('Checking record', record)
                if SpringCondition.UNKNOWN not in record:
                    if filtered_option := self._filter_option(record):
                        n_options += 1
                        # print('Filtered option', filtered_option)
                    continue

                for c in SpringCondition.DAMAGED, SpringCondition.OPERATIONAL:
                    new_record = record.replace(SpringCondition.UNKNOWN, c, 1)
                    # print('New record', new_record)

                    if filtered_option := self._filter_option(new_record, partial_ok=True):
                        record_queue.put(filtered_option)

            return n_options

        def _filter_option(self, option, partial_ok=False) -> str | None:

            if self._matches_groups(option, partial_ok):
                return option

        def _matches_groups(self, option, partial_ok):
            idx_0 = 0
            for amount in self.groups:

                if not (group_match := self._find_damaged(option, amount, idx_0)):
                    return False

                if SpringCondition.UNKNOWN in group_match.group(1):
                    if partial_ok:
                        return True
                    else:
                        return False

                if len(group_match.group(1)) != amount:
                    return False

                idx_0 = group_match.end()

            # Let's ensure there's nothing else
            if SpringCondition.DAMAGED in option[idx_0:]:
                return False

            return True

        @staticmethod
        def _find_damaged(option, amount, idx_0):
            return _RE_DAMAGED_SPRING.match(option, pos=idx_0)

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self.spring_rows = []

    def load_data(self, f):
        with f.open() as f_in:
            for line in f_in:
                record, groups = line.strip().split(' ')
                self.spring_rows.append(self.SpringRow(record, [int(x) for x in groups.split(',')]))

    def solve1(self):
        for row in self.spring_rows:
            self.logger.debug('Record %20s, Gr %s, N_Opts: %d', row.record, row.groups, row.n_options)
        return sum(row.n_options for row in self.spring_rows)

    def solve2(self):
        pass


if __name__ == '__main__':
    Problem()()
