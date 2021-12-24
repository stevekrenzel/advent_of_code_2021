from sys import stdin
from itertools import product
from dataclasses import dataclass

lines = [line.strip() for line in stdin.readlines()]

enhancement_key = lines[0]
pixels = lines[2:]

@dataclass(frozen=True)
class Grid:
    default: str
    pixels: list[str]
    width: int
    height: int

grid = Grid('.', pixels, len(pixels[0]), len(pixels))

def neighbors(x, y, grid):
    shifts = product([-1,0,1], [-1,0,1])

    for yd, xd in shifts:
        x_, y_ = x + xd, y + yd

        if (x_ < 0) or (y_ < 0):
            yield grid.default

        elif (x_ > grid.width - 1) or (y_ > grid.height - 1):
            yield grid.default

        else:
            yield grid.pixels[y_][x_]

def pixel_to_key(x, y, grid):
    bits = (0 if pixel == '.' else 1 for pixel in neighbors(x, y, grid))

    value = 0
    for bit in bits:
        value *= 2
        value += bit

    return value

def pad_grid(grid):
    default_row = [grid.default * (grid.width + 2)]
    padded = default_row + [grid.default + row + grid.default for row in grid.pixels] + default_row

    return Grid(grid.default, padded, grid.width + 2, grid.height + 2)

def enhance(enhancement_key, grid, times=1):
    if times == 0:
        return grid

    grid = pad_grid(grid)
    keys = [[pixel_to_key(x, y, grid) for x in range(grid.width)] for y in range(grid.height)]
    enhanced = [''.join(enhancement_key[key] for key in row) for row in keys]

    default = enhancement_key[0] if grid.default == '.' else enhancement_key[-1]
    grid = Grid(default, enhanced, grid.width, grid.height)

    return enhance(enhancement_key, grid, times - 1)

def count_lit_pixels(grid):
    return ''.join(grid.pixels).count('#')

enhanced = enhance(enhancement_key, grid, 2)
print(count_lit_pixels(enhanced))

enhanced = enhance(enhancement_key, grid, 50)
print(count_lit_pixels(enhanced))
