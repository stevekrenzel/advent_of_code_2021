from sys import stdin
from itertools import count

lines = [line.strip() for line in stdin.readlines()]
grid = [list(map(int, line)) for line in lines]

def neighbors(grid, x, y):
    if x > 0:
        yield (x - 1, y)
    if y > 0:
        yield (x, y - 1)
    if x > 0 and y > 0:
        yield(x - 1, y - 1)
    if x < len(grid) - 1:
        yield(x + 1, y)
    if y < len(grid[0]) - 1:
        yield(x, y + 1)
    if x < len(grid) - 1 and y < len(grid[0]) - 1:
        yield (x + 1, y + 1)
    if x > 0 and y < len(grid[0]) - 1:
        yield (x - 1, y + 1)
    if x < len(grid) - 1 and y > 0:
        yield (x + 1, y - 1)

def cells(grid):
    for x, row in enumerate(grid):
        for y, col in enumerate(row):
            yield (x, y, col)

def flash_cell(grid, x, y, flashed):
    if (x, y) in flashed:
        return

    if grid[x][y] < 10:
        return

    grid[x][y] += 1
    yield (x, y)

    for (x1, y1) in neighbors(grid, x, y):
        grid[x1][y1] += 1
        yield from flash_cell(grid, x1, y1, flashed)

def flash_grid(grid, flashed = None):
    grid = copy_grid(grid)
    flashed = flashed or set()

    for (x, y, _) in cells(grid):
        flashed.update(flash_cell(grid, x, y, flashed))

    return grid

def reset_flashed(grid):
    grid = copy_grid(grid)
    count = 0

    for (x, y, val) in cells(grid):
        if val > 9:
            grid[x][y] = 0
            count += 1

    return (grid, count)

def increment_grid(grid):
    grid = copy_grid(grid)

    for (x, y, val) in cells(grid):
        grid[x][y] = val + 1

    return grid

def step(grid):
    incremented = increment_grid(grid)
    flashed = flash_grid(incremented)
    (reset, count) = reset_flashed(flashed)

    return (reset, count)

def is_synchronized(grid):
    return all(val == 0 for (_, _, val) in cells(grid))

def copy_grid(grid):
    return [row[:] for row in grid]

def simulate(grid, days):
    total_flashes = 0

    for _ in range(days):
        (grid, flashes) = step(grid)
        total_flashes += flashes

    return total_flashes

def synchronization_day(grid):
    for i in count(1):
        (grid, _) = step(grid)
        if is_synchronized(grid):
            return i

print(simulate(grid, 100))
print(synchronization_day(grid))
