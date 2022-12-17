from sys import stdin
from collections import defaultdict
from bisect import insort, bisect_left as search
from enum import IntEnum, auto
from typing import NamedTuple, Optional

class Content(IntEnum):
    SOURCE = auto()
    AIR = auto()
    STONE = auto()
    SAND = auto()

class Coordinate(NamedTuple):
    x: int
    y: int

LineSegment = tuple[Coordinate, Coordinate]

Line = list[Coordinate]

class Cell(NamedTuple):
    position: Coordinate
    contents: Content

class DefaultDict(defaultdict):
    def __missing__(self, key):
        val = self.default_factory(key) # type: ignore
        self[key] = val
        return val

class World(NamedTuple):
    columns: DefaultDict
    start: Coordinate

    @staticmethod
    def new(start: Coordinate, lines: list[Line], floor: Optional[int] = None) -> 'World':
        bottom_y = max(p.y for segment in lines for p in segment)

        # Default dict will add a new column when needed, including floor if specified
        builder = lambda key: ([] if floor is None else [Cell(Coordinate(key, bottom_y + floor), Content.STONE)])
        columns = DefaultDict(builder) # type: ignore

        insort(columns[start.x], Cell(start, Content.SOURCE))

        world = World(columns, start)
        for line in lines:
            world.add_line(line)
        return world

    def count_grains(self: 'World') -> int:
        count = 0
        while self.add_grain():
            count += 1
        return count

    def add_grain(self: 'World') -> bool:
        resting_spot = self._find_sand_resting_spot(self.start)
        if resting_spot is None:
            return False

        cell = Cell(resting_spot, Content.SAND)
        insort(self.columns[cell.position.x], cell)
        return True

    def _find_sand_resting_spot(self: 'World', start: Coordinate) -> Optional[Coordinate]:
        column = self.columns[start.x]
        key = Cell(start, Content.AIR)
        index = search(column, key)
        if index >= len(column):
            return None

        blocker = column[index]
        resting_spot = Coordinate(blocker.position.x, blocker.position.y - 1)

        if self.is_blocked(resting_spot):
            return None

        left = Coordinate(resting_spot.x - 1, resting_spot.y + 1)
        right = Coordinate(resting_spot.x + 1, resting_spot.y + 1)

        if not self.is_blocked(left):
            resting_spot = self._find_sand_resting_spot(left)
        elif not self.is_blocked(right):
            resting_spot = self._find_sand_resting_spot(right)

        return resting_spot

    def is_blocked(self: 'World', coord: Coordinate) -> bool:
        column = self.columns[coord.x]
        key = Cell(coord, Content.AIR)
        index = search(column, key)

        if index >= len(column):
            return False

        return column[index].position == coord

    def add_line(self: 'World', line: Line) -> None:
        segments = zip(line, line[1:])
        for segment in segments:
            self.add_line_segment(segment)

    def add_line_segment(self: 'World', segment: LineSegment) -> None:
        start, end = segment

        if start.x > end.x or start.y > end.y:
            start, end = end, start

        for x in range(start.x, end.x + 1):
            for y in range(start.y, end.y + 1):
                cell = Cell(Coordinate(x, y), Content.STONE)
                insort(self.columns[x], cell)

def parse_line(line: str) -> Line:
    points = [point.split(',') for point in line.split(' -> ')]
    return [Coordinate(int(x), int(y)) for x, y in points]

lines = list(map(parse_line, stdin.read().splitlines()))
start = Coordinate(500, 0)

# Part 1
world = World.new(start, lines)
print(world.count_grains())

# Part 2
world = World.new(start, lines, 2)
print(world.count_grains() + 1)
