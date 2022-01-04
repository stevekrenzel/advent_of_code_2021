from sys import stdin
from math import prod

lines = [line.strip() for line in stdin.readlines()]
grid = [[int(cell) for cell in line] for line in lines]

def find_neighbors(grid, x, y):
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x < len(grid) - 1:
        yield (x + 1, y)
    if y < len(grid[0]) - 1:
        yield (x, y + 1)

def risk(grid, x, y):
    return 1 + grid[x][y]

def low_points(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            height = grid[x][y]
            neighbors = find_neighbors(grid, x, y)
            if all(height < grid[x1][y1] for  x1, y1 in neighbors):
                yield (x, y)

def find_basin(grid, x, y, visited = set()):
    if (x, y) in visited:
        return

    if grid[x][y] == 9:
        return

    visited.add((x, y))
    yield (x, y)

    for x1, y1 in find_neighbors(grid, x, y):
        yield from find_basin(grid, x1, y1, visited)

def all_basins(grid):
    for x, y in low_points(grid):
        yield list(find_basin(grid, x, y))

total_risk = sum(risk(grid, x, y) for x, y in low_points(grid))
basins = list(all_basins(grid))
basin_sizes = [len(basin) for basin in basins]
ordered_basins = sorted(basin_sizes)

print(total_risk)
print(prod(ordered_basins[-3:]))
