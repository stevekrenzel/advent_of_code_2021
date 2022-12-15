from sys import stdin
from heapq import heappop, heappush
from typing import NamedTuple, Optional, Iterable
from string import ascii_lowercase

class Position(NamedTuple):
    x: int
    y: int

    def neighbors(self, grid: 'Grid') -> Iterable['Position']:
        x, y = self

        if self.x > 0:
            yield Position(x - 1, y)

        if self.x < grid.width - 1:
            yield Position(x + 1, y)

        if self.y > 0:
            yield Position(x, y - 1)

        if self.y < grid.height - 1:
            yield Position(x, y + 1)

    def __str__(self: 'Position') -> str:
        return f'({self.x}, {self.y})'

Height = int

def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

class Grid(NamedTuple):
    start: Position
    end: Position
    heights: list[list[Height]]
    width: int
    height: int

    def find_shortest_path(self: 'Grid', start: Position) -> Optional[int]:
        # Uses A* for search
        heuristic = 0 + manhattan_distance(start, self.end)
        positions = [(heuristic, start, 0)]
        visited = set()

        while len(positions) > 0:
            _, position, traveled = heappop(positions)
            if position in visited:
                continue
            visited.add(position)

            if position == self.end:
                return traveled

            last_height = self.heights[position.y][position.x]
            for neighbor in position.neighbors(self):
                if neighbor in visited:
                    continue

                neighbor_height = self.heights[neighbor.y][neighbor.x]
                if neighbor_height > last_height + 1:
                    continue

                distance = manhattan_distance(neighbor, self.end)
                heuristic = traveled + distance
                heappush(positions, (heuristic, neighbor, traveled + 1))

        return None

    def find_best_start(self: 'Grid') -> Optional[int]:
        best = None
        for row in range(self.height):
            for col in range(self.width):
                height = self.heights[row][col]
                if height != 0:
                    continue

                distance = self.find_shortest_path(Position(col, row))
                if best is None or (distance is not None and distance < best):
                    best = distance
        return best


    @staticmethod
    def parse(lines: list[str]) -> 'Grid':
        start: Optional[Position] = None
        end: Optional[Position] = None
        heights: list[list[Height]] = []

        for y, line in enumerate(lines):
            heights.append([])
            for x, char in enumerate(line):
                if char == 'S':
                    start, char = Position(x, y), 'a'
                elif char == 'E':
                    end, char = Position(x, y), 'z'
                elif char not in ascii_lowercase:
                    raise Exception(f'Character {char} unknown how to parse.')

                height = ascii_lowercase.index(char)
                heights[-1].append(height)

        if start is None:
            raise Exception('Start is not specified')

        if end is None:
            raise Exception('end is not specified')

        width, height = len(heights[0]), len(heights)
        return Grid(start=start, end=end, width=width, height=height, heights=heights)

lines = stdin.read().splitlines()
grid = Grid.parse(lines)

# Part 1
print(grid.find_shortest_path(grid.start))

# Part 2
print(grid.find_best_start())
