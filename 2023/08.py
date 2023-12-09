"""2023-12-08 puzzle https://adventofcode.com/2023/day/8"""

import dataclasses
import re
from typing import Optional
import itertools
import math

import lib

START_NODE = 'AAA'
END_NODE = 'ZZZ'


@dataclasses.dataclass
class Node:
    name: str
    parent: Optional[str]
    left_child: str
    right_child: str

    @property
    def is_ghost_end(self):
        return self.name.endswith(END_NODE[-1])

    @property
    def is_end(self):
        return self.name == END_NODE[-1]

    @property
    def is_ghost_start(self):
        return self.name.endswith(START_NODE[-1])


RE_NODE = re.compile(r'(?P<parent>\w+) = \((?P<left>\w+), (?P<right>\w+)\)')


class Problem(lib.AOCProblem):
    """Solves the puzzle"""

    def __init__(self, **kwargs):
        super().__init__(dunder_file_child=__file__, **kwargs)

        self.instructions = None
        self.nodes = {}

    def load_data(self, f):
        with f.open() as f_in:

            self.instructions = f_in.readline().strip()

            for line in f_in:
                if not (line := line.strip()):
                    continue

                if not (match := RE_NODE.match(line)):
                    raise ValueError(f'Invalid node: {line}')

                parent_name, left, right = match.groups()
                self.nodes[parent_name] = Node(parent_name, None, left, right)

    def post_load(self):
        self.logger.debug('Instructions: "%s"', self.instructions)
        self._join_nodes()

    def _join_nodes(self):
        for node in self.nodes.values():
            self.nodes[node.left_child].parent = node.name
            self.nodes[node.right_child].parent = node.name

    def _print_nodes(self, nodes):
        nodes = nodes or self.nodes.values()
        self.logger.debug('Nodes:')
        for node in nodes:
            self.logger.debug('\t\t%s', node)

    def solve1(self):

        if not (iter_node := self.nodes.get(START_NODE, None)):
            return  # Some tests for part 2 don't have a start node compatible with part 1

        for i, instruction in enumerate(itertools.cycle(self.instructions)):

            if not (iter_node := self._iter_node(iter_node, instruction)):
                return i

    def solve2(self):
        iter_nodes = {idx: node for idx, node in enumerate(self.nodes.values()) if node.is_ghost_start}

        for idx, node in iter_nodes.items():
            self.logger.debug('Node %s: %s', idx, node)
        offsets = {}
        periods = {}

        for idx, iter_node in iter_nodes.items():

            offset_to_be_found = True
            for i, instruction in enumerate(itertools.cycle(self.instructions), start=1):

                if (iter_node := self._iter_node(iter_node, instruction, end_node=False)).is_ghost_end:

                    if offset_to_be_found:
                        offsets[idx] = i
                        offset_to_be_found = False

                        self.logger.debug('Offsets: %s', offsets)

                        continue

                    periods[idx] = i - offsets[idx]
                    break

        self.logger.debug('Offsets: %s', offsets)
        self.logger.debug('Periods: %s', periods)

        return math.lcm(*[int(x) for x in periods.values()])

    def _iter_node(self, node: Node, instruction: str, end_node=True):

        if end_node and node.name == END_NODE:
            return None

        if instruction == 'L':
            next_node = self.nodes[node.left_child]
        elif instruction == 'R':
            next_node = self.nodes[node.right_child]
        else:
            raise ValueError(f'Invalid instruction: {instruction}')

        return next_node


if __name__ == '__main__':
    Problem(test=False)()
