from sys import stdin
from itertools import combinations

# Parsing input
lines = stdin.read().splitlines()
width, height = len(lines[0]), len(lines)

marked_columns = [i for i in range(width) if all(line[i] == '.' for line in lines)]
marked_rows = [i for i in range(height) if all(c == '.' for c in lines[i])]
galaxy_locations = [(x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == '#']

def manhattan_distance(a, b, expansion_factor):
    rows = list(range(min(a[1], b[1]), max(a[1], b[1]) + 1))
    cols = list(range(min(a[0], b[0]), max(a[0], b[0]) + 1))

    total = 0
    for row in rows:
        total += expansion_factor if row in marked_rows else 1
    for col in cols:
        total += expansion_factor if col in marked_columns else 1
    return total - 2

# Part 1
print(sum(manhattan_distance(a, b, 2) for a, b in combinations(galaxy_locations, 2)))

# Part 2
print(sum(manhattan_distance(a, b, 1000000) for a, b in combinations(galaxy_locations, 2)))
