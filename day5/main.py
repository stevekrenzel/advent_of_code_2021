from sys import stdin
from collections import Counter
from itertools import chain

lines = [line.strip() for line in stdin.readlines()]
pairs = [line.split(' -> ') for line in lines]

to_ints = lambda xs: [int(x) for x in xs]
segments = [(to_ints(a.split(',')), to_ints(b.split(','))) for (a, b) in pairs]

def isLateral(segment):
    ((x1, y1), (x2, y2)) = segment
    return x1 == x2 or y1 == y2

def cmp(a, b):
    return (a > b) - (a < b)

def points(segment):
    (start, end) = segment
    (x1, y1) = start
    (x2, y2) = end

    x_inc = -1 * cmp(x1, x2)
    y_inc = -1 * cmp(y1, y2)

    (x, y) = (x1, y1)
    while x != x2 + x_inc or y != y2 + y_inc:
        yield (x, y)
        (x, y) = (x + x_inc, y + y_inc)

laterals = filter(isLateral, segments)
lateral_points = chain(*map(points, laterals))
lateral_counts = Counter(lateral_points)
lateral_dangerous = sum(1 for (_, count) in lateral_counts.items() if count >= 2)
print(lateral_dangerous)

all_points = chain(*map(points, segments))
all_counts = Counter(all_points)
all_dangerous = sum(1 for (_, count) in all_counts.items() if count >= 2)
print(all_dangerous)
