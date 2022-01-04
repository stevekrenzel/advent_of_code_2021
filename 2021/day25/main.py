from sys import stdin

grid = [list(line.strip()) for line in stdin.readlines()]

def step(grid):
    return step_south(step_east(grid))

def step_east(grid):
    width = len(grid[0])
    new_grid = [row[:] for row in grid]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '>':
                neighbor = (x+1) % width
                if grid[y][neighbor] == '.':
                    new_grid[y][x] = '.'
                    new_grid[y][neighbor] = '>'

    return new_grid

def step_south(grid):
    height = len(grid)
    new_grid = [row[:] for row in grid]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'v':
                neighbor = (y+1) % height
                if grid[neighbor][x] == '.':
                    new_grid[y][x] = '.'
                    new_grid[neighbor][x] = 'v'

    return new_grid

def converge(grid):
    steps = 0

    while True:
        new_grid = step(grid)
        steps += 1
        if new_grid == grid:
            return steps, new_grid
        grid = new_grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

steps, _ = converge(grid)
print(steps)
