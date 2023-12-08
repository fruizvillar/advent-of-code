import dataclasses

import lib


class RangeConversion:

    def __init__(self, dst_range_start: int, src_range_start: int, length: int):
        self.src_range = lib.Range(src_range_start, length)
        self.dst_range = lib.Range(dst_range_start, length)
        self.offset = dst_range_start - src_range_start
        self.length = length

    def is_in_src(self, value: int) -> bool:
        return value in self.src_range

    def convert(self, value: int) -> int:
        return value + self.offset

    def interval_repr(self):
        return f'{self.src_range.start}-{self.src_range.end} -> {self.dst_range.start}-{self.dst_range.end}'

    def dst_src_overlapping(self, other_range_conversion):
        """Returns the overlapping range in the dst space, or None if there is no overlapping"""

        other_range = other_range_conversion.src_range

        return self.dst_range.overlapping(other_range)

    def dst_src_remainders(self, other_range_conversion):
        """Returns the non-overlapping ranges in the dst space"""
        this_range = self.dst_range

        if not (overlapping_range := self.dst_src_overlapping(other_range_conversion)):
            return [this_range]

        overlaps = []

        if this_range.start < overlapping_range.start:
            overlaps.append(lib.Range(this_range.start, overlapping_range.start - this_range.start))

        if this_range.end > overlapping_range.end:
            overlaps.append(lib.Range(overlapping_range.end + 1, this_range.end - overlapping_range.end))

        return overlaps

    def with_start(self, start):
        """Returns a new RangeConversion that goes from the given value to the end of this one"""
        if start > self.src_range.end:
            raise RuntimeError(f'Value {start} is after the end of the range {self.src_range.end}')
        new_length = self.src_range.end - start + 1
        return RangeConversion(self.dst_range.start + start - self.src_range.start, start, new_length)

    def with_end(self, end):
        """Returns a new RangeConversion that goes from the start of this one to the given value"""
        if end < self.src_range.start:
            raise RuntimeError(f'Value {end} is before the start of the range {self.src_range.start}')
        return RangeConversion(self.dst_range.start, self.src_range.start, end - self.src_range.start + 1)

    def __repr__(self):
        return (f'{self.src_range.start:02}-{self.src_range.end:02} --({self.offset:+3d})--> {self.dst_range.start:02}'
                f'-{self.dst_range.end:02}')


@dataclasses.dataclass
class RangeMap:
    src: str
    dst: str
    ranges: list[RangeConversion] = dataclasses.field(default_factory=list)

    @property
    def name(self):
        return f'{self.src}-to-{self.dst}'

    def add(self, range_conversion: RangeConversion):
        self.ranges.append(range_conversion)
        self._sort()
        self._check()

    def add_all(self, range_conversions: list[RangeConversion]):
        self.ranges.extend(range_conversions)
        self._sort()
        self._check()

    def convert(self, value: int) -> int:
        for r in self.ranges:
            if r.is_in_src(value):
                return r.convert(value)

        # No match -> convert(x) = x
        return value

    def _sort(self):
        self.ranges.sort(key=lambda r: r.src_range.start)

    def _check(self):
        prev_r = None
        for r in self.ranges:
            if prev_r is None:
                prev_r = r
                continue

            if prev_r.src_range.end >= r.src_range.start:
                raise RuntimeError(f'Range {prev_r} overlaps with {r}')
            prev_r = r

    def combine(self, other) -> 'RangeMap':
        """Combines two maps into a new one"""
        if self.dst != other.src:
            raise RuntimeError(f'Cannot combine maps {self.name} and {other.name}')

        combined_map = RangeMap(self.src, other.dst)

        a_ranges = sorted(self.ranges.copy(), key=lambda r: r.dst_range.start)
        b_ranges = other.ranges.copy()

        there_are_overlaps = None
        while there_are_overlaps is not False:
            there_are_overlaps = False

            a_ranges_new = a_ranges.copy()
            b_ranges_new = b_ranges.copy()

            for a_range in a_ranges:
                for b_range in b_ranges:

                    if b_range not in b_ranges_new:
                        continue  # Overlap has already been checked for another a_range

                    a = a_range.dst_range
                    b = b_range.src_range

                    if not (overlap := a.overlapping(b)):
                        continue

                    there_are_overlaps = True

                    a_ranges_new.remove(a_range)
                    b_ranges_new.remove(b_range)

                    overlap_range = RangeConversion(
                        src_range_start=overlap.start - a_range.offset,
                        dst_range_start=overlap.start + b_range.offset,
                        length=overlap.length
                    )

                    if overlap_range.offset:
                        combined_map.add(overlap_range)
                    else:
                        combined_map.add(overlap_range)

                    # Pre-overlap
                    if a.start < b.start:
                        pre_overlap_a_range = a_range.with_end(overlap.start - a_range.offset - 1)
                        a_ranges_new.append(pre_overlap_a_range)

                    elif a.start > b.start:
                        pre_overlap_b_range = b_range.with_end(overlap.start - 1)
                        b_ranges_new.append(pre_overlap_b_range)

                    # Post-overlap
                    if a.end > b.end:
                        post_overlap_a_range = a_range.with_start(overlap.end - a_range.offset + 1)
                        a_ranges_new.append(post_overlap_a_range)

                    elif a.end < b.end:
                        post_overlap_b_range = b_range.with_start(overlap.end + 1)
                        b_ranges_new.append(post_overlap_b_range)

                    break  # We already found an overlap for this a_range

            a_ranges = a_ranges_new
            b_ranges = b_ranges_new

        for r in a_ranges:
            combined_map.add(r)
        for r in b_ranges:
            combined_map.add(r)

        return combined_map


class Problem(lib.AOCProblem):
    """2023/05 puzzle https://adventofcode.com/2023/day/5"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)

        self.seeds = []
        self.range_maps = {}
        self.thin_range_map = None

    def load_data(self, f):
        with f.open() as f_in:
            self.seeds = [int(n) for n in f_in.readline().strip().split(':')[1].split(' ') if n]

            range_map = None

            for line in f_in:

                if 'map' in line:
                    map_name = line.split(' ')[0].strip()
                    src, _, dst = [s for s in map_name.split('-')]
                    range_map = RangeMap(src, dst)
                    continue

                if not line.strip():
                    if range_map:
                        self.range_maps[range_map.src] = range_map
                        range_map = None

                    continue

                if not range_map:
                    raise RuntimeError('No map defined')

                range_map.add(RangeConversion(*[int(n) for n in line.strip().split(' ')]))

            if range_map:
                self.range_maps[range_map.src] = range_map

    def solve1(self):

        locations = []

        for seed in self.seeds:

            # No thin map, hence we need to convert the seed to the location
            current_info = 'seed'
            current_value = seed
            while current_info != 'location':
                next_map = self.range_maps[current_info]
                new_value = next_map.convert(current_value)
                new_info = next_map.dst
                current_info = new_info
                current_value = new_value

            locations.append(current_value)

        return min(locations) if locations else None

    def solve2(self):
        self._thin_map()

        seed_intervals = self._get_seed_ranges()

        edge_locations = []

        for interval in seed_intervals:

            for map_src_interval in self.thin_range_map.ranges:
                if not (overlap := interval.overlapping(map_src_interval.src_range)):
                    continue


                edge_locations.append(map_src_interval.convert(overlap.start))
                edge_locations.append(map_src_interval.convert(overlap.end))


        return min(edge_locations)

    def _get_seed_ranges(self):
        ranges = []
        first_seed = length = None
        for seed_or_length in self.seeds:

            if first_seed is None:
                first_seed = seed_or_length
                continue

            if length is None:
                length = seed_or_length

            ranges.append(lib.Range(first_seed, length))
            first_seed = length = None

        return ranges

    def _thin_map(self):
        """If the map is thin, we can quickly convert the seeds to the locations"""
        if self.thin_range_map:
            return


        type_src = 'seed'

        combined_map = self.range_maps[type_src]

        while next_map := self.range_maps.get(combined_map.dst, None):
            combined_map = combined_map.combine(next_map)

        self.thin_range_map = combined_map


if __name__ == '__main__':
    Problem()()
