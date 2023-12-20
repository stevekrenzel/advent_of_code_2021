from sys import stdin

# Parsing input
lines = [list(map(int, line.split(' '))) for line in stdin.read().splitlines()]

def differences(xs):
    ds = [xs]
    while any(d != 0 for d in ds[-1]):
        prev = ds[-1]
        nxt = [b - a for a, b in zip(prev, prev[1:])]
        ds.append(nxt)
    return ds

def extend(ds):
    es = [d[:] for d in ds]
    es[-1].insert(0, 0)
    es[-1].append(0)

    for i in range(len(es) - 2, -1, -1):
        es[i].insert(0, es[i][0] - es[i + 1][0])
        es[i].append(es[i][-1] + es[i + 1][-1])

    return es

# Part 1
total = 0
for line in lines:
    diffs = differences(line)
    extended = extend(diffs)
    total += extended[0][-1]
print(total)

# Part 2
total = 0
for line in lines:
    diffs = differences(line)
    extended = extend(diffs)
    total += extended[0][0]
print(total)
