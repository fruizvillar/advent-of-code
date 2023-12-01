from pathlib import Path
from queue import LifoQueue
from typing import Dict

from lib import AOCProblem


class TodaysProblem(AOCProblem):
    N = 7

    PROMPT = '$'

    SIZE_THR = 100_000

    TOTAL_SIZE = 70_000_000
    TARGET_FREE = 30_000_000

    class AocFileItem:
        def __init__(self, parent: 'TodaysProblem.Dir' = None, name: str = '/'):
            self.name = name
            if parent is None:
                self.path = Path('/')
            else:
                self.path = parent.path / name
            self.parent = parent  # type:

        @property
        def _depth(self) -> int:
            return len(list(self.path.parents))

        def __str__(self):
            return '  ' * self._depth + f'- {self.name}'

    class Dir(AocFileItem):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.children = {}  # type: Dict[TodaysProblem.Dir]
            self.content_size = 0

        def __str__(self):
            return super().__str__() + ' (dir)'

    class AocFile(AocFileItem):
        def __init__(self, parent, name: str, size: int):
            super().__init__(parent, name)
            self.size = int(size)

        def __str__(self):
            return super().__str__() + f' (file, size={self.size})'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dirs = []
        self.commands = []
        self.root = self.Dir()
        self.cwd = self.root  # type: TodaysProblem.Dir

    def load_data(self, f: Path):
        with f.open() as buffer:
            for line in buffer.readlines():
                segments = line.split()
                self.commands.append(segments)

        for line in self.commands:
            if line[0] == self.PROMPT:
                if line[1] == 'ls':
                    continue  # items follow

                if line[1] == 'cd':
                    dir_name = line[2]
                    if dir_name == '..':
                        new_path = self.cwd.parent
                    elif dir_name == '/':
                        new_path = self.root
                    else:
                        new_path = self.cwd.children[dir_name]

                    self.cwd = new_path
                    continue

                print(f'UNKNOWN COMMAND {line[1]}')
                continue

            item_name = line[1]
            if line[0] == 'dir':
                item = self.Dir(self.cwd, item_name)
            else:
                item = self.AocFile(self.cwd, item_name, line[0])

            self.cwd.children[item_name] = item

        self._load_dir_sizes()

    def solve1(self):

        inspect_q = LifoQueue()
        inspect_q.put_nowait(self.root)

        while not inspect_q.empty():
            item = inspect_q.get_nowait()

            if isinstance(item, self.Dir):
                self.dirs.append(item)

                for child_name, child in item.children.items():
                    inspect_q.put_nowait(child)

        small_dirs = [d for d in self.dirs if d.content_size <= self.SIZE_THR]

        return sum(d.content_size for d in small_dirs)

    def solve2(self):

        total_used = self.root.content_size

        total_unused = self.TOTAL_SIZE - total_used

        need_to_free_up = self.TARGET_FREE - total_unused

        if need_to_free_up <= 0:
            return 0

        d_to_free_up = sorted((d for d in self.dirs if d.content_size >= need_to_free_up), key=lambda d: d.content_size)

        return d_to_free_up[0].content_size

    def _load_dir_sizes(self):
        inspect_q = LifoQueue()
        inspect_q.put_nowait(self.root)

        while not inspect_q.empty():
            item = inspect_q.get_nowait()

            if isinstance(item, self.Dir):
                for child_name, child in item.children.items():
                    inspect_q.put_nowait(child)

            elif isinstance(item, self.AocFile):
                this_size = item.size
                while item.parent:
                    item.parent.content_size += this_size
                    item = item.parent

    def _print(self):

        inspect_q = LifoQueue()
        inspect_q.put_nowait(self.root)

        while not inspect_q.empty():
            item = inspect_q.get_nowait()

            if isinstance(item, self.Dir):
                for child_name, child in item.children.items():
                    inspect_q.put_nowait(child)


if __name__ == '__main__':
    TodaysProblem(test=False)()
