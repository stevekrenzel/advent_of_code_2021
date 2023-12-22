from sys import stdin
from typing import NamedTuple
from collections import defaultdict

Coordinate = tuple[int, int]

class Grid(NamedTuple):
    width: int
    height: int
    start: Coordinate
    connections: dict[Coordinate, list[Coordinate]]

    def longest_path(self: 'Grid') -> int:
        starting_connections = self.connections[self.start]
        queued = [(self.start, neighbor) for neighbor in starting_connections]
        distances = {self.start: 0}

        while len(queued) > 0:
            prev, current = queued.pop(0)
            if current in distances:
                continue

            distances[current] = distances[prev] + 1
            for neighbor in self.connections[current]:
                queued.append((current, neighbor))

        return max(distances.values())

    def main_loop(self: 'Grid') -> [Coordinate]:
        next_node = self.connections[self.start][0]
        loop_nodes = [self.start, next_node]
        while loop_nodes[-1] != loop_nodes[0]:
            for neighbor in self.connections[loop_nodes[-1]]:
                if neighbor in loop_nodes:
                    continue
                loop_nodes.append(neighbor)
                break
            else:
                break
        return set(loop_nodes)

    def area(self: 'Grid') -> [[Coordinate]]:
        loop, seen = self.main_loop(), set()

        for coord in self.connections:
            if coord in seen or coord in loop:
                continue

            queued = [coord]
            is_island, island = True, []
            while len(queued) > 0:
                (x, y) = queued.pop(0)

                if (x, y) in seen:
                    continue
                seen.add((x, y))


                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    is_island = False
                    continue

                # Hit a pipe
                direct_hit = (x, y) in loop
                vertical_extension = (x, y + 0.5) in loop and (x, y - 0.5) in loop and (x, y + 0.5) in self.connections.get((x, y - 0.5), []) and (x, y - 0.5) in self.connections.get((x, y + 0.5), [])
                horizontal_extension = (x + 0.5, y) in loop and (x - 0.5, y) in loop and (x + 0.5, y) in self.connections.get((x - 0.5, y), []) and (x - 0.5, y) in self.connections.get((x + 0.5, y), [])
                if direct_hit or vertical_extension or horizontal_extension:
                    continue

                # This may be part of an island
                island.append((x, y))

                # Explore neighbors
                queued.extend([
                    (x + 0, y + 0.5),
                    (x + 0, y - 0.5),
                    (x - 0.5, y + 0),
                    (x + 0.5, y + 0)
                ])
            if is_island:
                return len([(x, y) for (x, y) in island if int(x) == x and int(y) == y])

    @staticmethod
    def parse(lines: [str]) -> 'Grid':
        start, connections = None, dict()
        width, height = len(lines[0]), len(lines)

        # Parse grid
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                point = (x, y)

                if val == 'S':
                    start = point

                neighbors = Grid.neighbors(point, val)
                connections[point] = neighbors

        # Back-fill start connections
        if start is None:
            raise ValueError('No start found')
        start_neighbors = [cell for cell, neighbors in connections.items() for coord in neighbors if coord == start]
        connections[start] = start_neighbors

        return Grid(width, height, start, connections)

    @staticmethod
    def neighbors(coordinate: Coordinate, val: str) -> [Coordinate]:
        x, y = coordinate
        if val == '|':
            return [(x + 0, y - 1), (x + 0, y + 1)]
        if val == '-':
            return [(x - 1, y + 0), (x + 1, y + 0)]
        if val == 'L':
            return [(x + 0, y - 1), (x + 1, y + 0)]
        if val == 'J':
            return [(x + 0, y - 1), (x - 1, y + 0)]
        if val == '7':
            return [(x - 1, y + 0), (x + 0, y + 1)]
        if val == 'F':
            return [(x + 1, y + 0), (x + 0, y + 1)]
        return []

# Parsing input
lines = stdin.read().splitlines()
grid = Grid.parse(lines)

# Part 1
print(grid.longest_path())

# Part 2
print(grid.area())
