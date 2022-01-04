from sys import stdin
from heapq import heappush, heappop

lines = [line.strip() for line in stdin.readlines()]
grid = [list(map(int, line)) for line in lines]

def neighbors(grid, node, scale=1):
    x, y = node
    w = width(grid, scale)
    h = height(grid, scale)

    if x > 0:
        yield (x - 1, y)
    if x < w - 1:
        yield (x + 1, y)
    if y > 0:
         yield (x, y - 1)
    if y < h - 1:
        yield (x, y + 1)

def risk(grid, node):
    w, h = width(grid), height(grid)
    x, y = node

    origin_x, origin_y = x % w, y % h
    delta_x, delta_y = abs(origin_x - x) , abs(origin_y - y)

    origin_risk = grid[origin_y][origin_x]
    shifted_risk = origin_risk + (delta_x // w) + (delta_y // h)

    return shifted_risk % 10

def width(grid, scale=1):
    return len(grid[0]) * scale

def height(grid, scale=1):
    return len(grid) * scale

def least_risk(grid, scale=1):
    w = width(grid, scale)
    h = height(grid, scale)

    start = (0,0)
    end = (w - 1, h - 1)

    exploring = [(risk(grid, start), start)]
    visited = set(start)

    while len(exploring) > 0:
        (current_risk, current_node) = heappop(exploring)

        if current_node == end:
            return current_risk - risk(grid, start)

        for neighbor in neighbors(grid, current_node, scale):

            if neighbor in visited:
                continue
            visited.add(neighbor)

            new_risk = current_risk + risk(grid, neighbor)
            heappush(exploring, (new_risk, neighbor))

    return None

print(least_risk(grid))
print(least_risk(grid, scale=5))
