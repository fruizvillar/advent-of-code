import enum
from typing import Optional

import lib
import logging
import queue

import colorama


@enum.unique
class Pixel(enum.StrEnum):
    """ Names determine behaviour. Do not change them without thorough testing"""
    N_S_V_PIPE = '|'
    W_E_H_PIPE = '-'
    N_E_90_DEG = 'L'
    N_W_90_DEG = 'J'
    S_W_90_DEG = '7'
    S_E_90_DEG = 'F'
    GROUND = '.'
    START = 'S'

    def connects_with(self, other: 'Pixel', direction: Optional[lib.Coordinate2D] = None):

        if not self.may_connect_with(other):
            logging.debug(f'Connects {self} with {other} in {direction}? NO')
            return False
        if not direction:
            logging.debug(f'Connects {self} with {other} in {direction}? TRUE')
            return True

        direction_other = - direction

        if self != self.START and direction.name not in self.name[:3]:
            logging.debug(f'Connects {self} with {other} in {direction}? NO')
            return False
        if other != self.START and direction_other.name not in other.name[:3]:
            logging.debug(f'Connects {self} with {other} in {direction}? NO')
            return False

        logging.debug(f'Connects {self} with {other} in {direction}? TRUE')
        return True

    def may_connect_with(self, other):
        """Whether two pipes may connect, regardless of the direction"""
        if self == self.GROUND or other == self.GROUND:
            return False
        if self == self.START or other == self.START:
            return True  # We don't know so we can't say no

        # pipes without a bend may connect with any other pipe except for the dual ('|' --X--> '-') nor vice versa
        if self == self.N_S_V_PIPE:
            return other != self.W_E_H_PIPE
        if self == self.W_E_H_PIPE:
            return other != self.N_S_V_PIPE

        return self != other


class Diagram:
    class Element:
        def __init__(self, pixel: Pixel, y, x, _meta=None):
            self.pixel = pixel
            self.pos = lib.Position2D(y, x)
            self._meta = _meta or {}

        def __str__(self):
            return f'E({self.pixel.value}, {self.pos})'

        def __repr__(self):
            return f'{self.__class__.__name__}({self.pixel})'

        def __lt__(self, other):
            return self.pos < other.pos

    def __init__(self, diagram_matrix):

        self._matrix = []
        for y, row in enumerate(diagram_matrix):
            element_row = []
            for x, pixel in enumerate(row):
                element = self.Element(pixel, y, x)
                if pixel == Pixel.START:
                    self.start = element

                element_row.append(element)

            self._matrix.append(element_row)

    def __str__(self):
        return '\n'.join([''.join(e.pixel for e in line) for line in self._matrix])

    @property
    def size(self):
        return len(self._matrix), len(self._matrix[0])

    def unicode(self):
        self_repr = str(self)

        for replace_pair in (
                ('|', '‖'),
                ('-', '═'),
                ('L', '╚'),
                ('J', '╝'),
                ('7', '╗'),
                ('F', '╔'),
                ('.', ' '),
                ('S', '╬'),
        ):
            self_repr = self_repr.replace(*replace_pair)

        return self_repr

    def __iter__(self):
        yield from self._matrix

    def __getitem__(self, instance):
        if isinstance(instance, (lib.Coordinate2D, lib._Base2D)):
            y = instance.y
            x = instance.x

        elif isinstance(instance, tuple):
            y = instance[0]
            x = instance[1]
        else:
            raise TypeError(f'Invalid index type: {type(instance)}')

        if y < 0 or x < 0:
            raise IndexError(f'Negative index: {y}, {x}')
        return self._matrix[y][x]


class Node:
    def __init__(self, element, nxt=None, prev=None, _meta=None):
        self.element = element
        self.next = nxt
        self.prev = prev
        self._meta = _meta or {}

    def __str__(self):
        return f'N({self.element})'


class Problem(lib.AOCProblem):
    """2023-12-10 puzzle https://adventofcode.com/2023/day/10"""

    def __init__(self, test=False, verbose=False):
        super().__init__(dunder_file_child=__file__, test=test, verbose=verbose)
        self._s_loop_start = None
        self.diagram = None
        self._start = None
        self.distances = {}
        self.pipe = []

    def load_data(self, f):
        diagram = []
        with f.open() as f_in:
            for line in f_in:
                diagram.append([Pixel(s) for s in line.strip()])

        self.diagram = Diagram(diagram)

    def solve1(self):
        logging.debug('Diagram:\n%s', self.diagram)
        logging.debug('Diagram:\n%s', self.diagram.unicode())
        self._find_s_loop()

        max_d = 0

        for node, distance in self.distances.items():
            logging.debug(f'{node}: {distance}')
            if distance > max_d:
                max_d = distance

        logging.debug('Diagram:\n%s', self.diagram.unicode())
        return max_d

    def solve2(self):
        surrounded_nodes = set()

        diagram_contour = sorted(set(
            [self.diagram[(0, x)] for x in range(self.diagram.size[1])]+
            [self.diagram[(y, 0)] for y in range(1, self.diagram.size[0])]
        ))

        for element in diagram_contour:
            self.logger.debug('Element: %s', element, )

            exit_found = False

            if element in self.pipe:
                continue

            for coordinate in lib.Coordinate:
                if exit_found:
                    break

                next_pos = element.pos + coordinate
                while True:
                    try:
                        self.logger.debug('Element: %s. Next pos: %s', element, next_pos)
                        if self.diagram[next_pos] != Pixel.GROUND:
                            break

                    except IndexError:
                        # Found an exit
                        exit_found = True
                        break

                    next_pos = element.pos + coordinate

            if not exit_found:
                surrounded_nodes.add(element.pos)

        print()
        self._print_colours(surrounded_nodes)

        return len(surrounded_nodes)

    def _find_s_loop(self):
        if self._s_loop_start:
            return self._s_loop_start

        start_node = Node(self.diagram.start)
        self._start = start_node
        logging.debug(f'Start: {start_node}')
        self.pipe.append(self.diagram.start.pos)

        node_queue = queue.Queue()

        node_queue.put((start_node, 0))
        visited_node_pos_distance = {start_node.element.pos: 0}
        board_size = self.diagram.size

        while not node_queue.empty():
            logging.debug(f'Queue: {node_queue.queue}')

            node, distance = node_queue.get()
            next_distance = distance + 1

            for direction, next_node_pos in node.element.pos.iter_direction_neighbours(filter_out_of_bounds=board_size,
                                                                                       use_coordinates=True):

                if (next_element := self.diagram[next_node_pos]).pixel == Pixel.GROUND:
                    continue
                if not node.element.pixel.connects_with(next_element.pixel, direction):
                    continue

                next_node = Node(next_element, _meta={'distance': next_distance})

                if next_node_pos in visited_node_pos_distance:
                    if visited_node_pos_distance[next_node_pos] <= distance:
                        logging.debug(f'Already visited {next_node_pos}')

                        continue
                    else:
                        logging.debug(f'Shortcut found to {next_node_pos}')

                node.next = next_node
                next_node.prev = node
                visited_node_pos_distance[next_node_pos] = next_distance
                self.pipe.append(next_node_pos)
                node_queue.put((next_node, next_distance))

        self._print_colours()

        self.distances = visited_node_pos_distance

    def _print_colours(self, inside_nodes=None):
        inside_nodes = inside_nodes or set()
        colorama.init()
        for y, bw_line in enumerate(self.diagram.unicode().splitlines()):
            colour_line = []
            for x, char in enumerate(bw_line):
                if (y, x) in self.pipe:
                    colour_line.append(colorama.Fore.GREEN + char + colorama.Style.RESET_ALL)
                elif (y, x) in inside_nodes:
                    colour_line.append(colorama.Fore.RED + char + colorama.Style.RESET_ALL)
                else:
                    colour_line.append(char)

            print(*colour_line, sep='')


if __name__ == '__main__':
    Problem(test=True, verbose=True)()
