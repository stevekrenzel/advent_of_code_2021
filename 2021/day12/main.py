from sys import stdin
from collections import defaultdict, Counter

pairs = [line.strip().split('-') for line in stdin.readlines()]

def make_graph(pairs):
    adjaceny_list = defaultdict(list)

    for start, end in pairs:
            adjaceny_list[start].append(end)
            adjaceny_list[end].append(start)

    return adjaceny_list

def all_paths(graph, check, start='start', end='end', path=None):
    if path is None:
        path = [start]

    if check(path) == False:
        return

    last = path[-1]
    if last == end:
        yield path
        return

    for edge in graph[last]:
        yield from all_paths(graph, check, start, end, path + [edge])

def is_small_cave(cave):
    return str.islower(cave)

def small_caves_once_filter(path):
    counts = Counter(path)

    for cave, count in counts.items():
        if is_small_cave(cave) == False:
            continue

        if count > 1:
            return False

    return True

def small_caves_twice_filter(path):
    counts = Counter(path)
    doubles = 0

    for cave, count in counts.items():
        if is_small_cave(cave) == False:
            continue

        if count > 2:
            return False

        if cave == 'start' and count > 1:
            return False

        if cave == 'end' and count > 1:
            return False

        if count == 2:
            doubles += 1

        if doubles > 1:
            return False

    return True

graph = make_graph(pairs)
print(sum(1 for _ in all_paths(graph, small_caves_once_filter)))
print(sum(1 for _ in all_paths(graph, small_caves_twice_filter)))
