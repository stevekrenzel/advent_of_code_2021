from sys import stdin
from typing import NamedTuple, Iterable

Volume = set['Voxel']

class Voxel(NamedTuple):
    x: int
    y: int
    z: int

    def neighbors(self: 'Voxel') -> Iterable['Voxel']:
        yield Voxel(self.x - 1, self.y, self.z)
        yield Voxel(self.x + 1, self.y, self.z)
        yield Voxel(self.x, self.y - 1, self.z)
        yield Voxel(self.x, self.y + 1, self.z)
        yield Voxel(self.x, self.y, self.z - 1)
        yield Voxel(self.x, self.y, self.z + 1)

    def exposed_area(self: 'Voxel', volume: Volume) -> int:
        return sum(1 for neighbor in self.neighbors() if neighbor not in volume)

    def covered_area(self: 'Voxel', volume: Volume) -> int:
        return sum(1 for neighbor in self.neighbors() if neighbor in volume)

    @staticmethod
    def parse(line: str) -> 'Voxel':
        return Voxel(*map(int, line.split(',')))

def perimeter(volume: Volume) -> Iterable['Voxel']:
    # Get the bounding cube of the voxels
    min_x, max_x = min(x for x, _, _ in volume) - 1, max(x for x, _, _ in volume) + 1
    min_y, max_y = min(y for _, y, _ in volume) - 1, max(y for _, y, _ in volume) + 1
    min_z, max_z = min(z for _, z, _ in volume) - 1, max(z for _, _, z in volume) + 1

    searched = set()
    corner = Voxel(min_x, min_y, min_z)
    stack = list(corner.neighbors())
    while len(stack) > 0:
        voxel = stack.pop()

        if voxel in searched:
            continue
        searched.add(voxel)

        if not (min_x <= voxel.x <= max_x):
            continue

        if not (min_y <= voxel.y <= max_y):
            continue

        if not (min_z <= voxel.z <= max_z):
            continue

        if voxel in volume:
            continue

        if voxel.covered_area(volume) > 0:
            yield voxel

        stack.extend(voxel.neighbors())

voxels = set(map(Voxel.parse, stdin.read().splitlines()))

# Part 1
print(sum(voxel.exposed_area(voxels) for voxel in voxels))

# Part 2
print(sum(voxel.covered_area(voxels) for voxel in perimeter(voxels)))
