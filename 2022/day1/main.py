from sys import stdin
from itertools import groupby

lines = stdin.read().splitlines()
groups = [list(group) for key, group in groupby(lines, bool) if key]
elves = [sum(map(int, group)) for group in groups]

elves = sorted(elves, reverse=True)

print(elves[0])
print(sum(elves[:3]))
