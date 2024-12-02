from sys import stdin
from collections import Counter

# Raw lines from input
lines = stdin.readlines()

# Split each line into a list of strings
# (e.g. ["1 2 3 4", "5 6 7 8"] -> [["1", "2", "3", "4"], ["5", "6", "7", "8"]])
reports = [[int(x) for x in line.strip().split()] for line in lines]


def is_safe(report):
    # Is monotonically increasing or decreasing
    if report != sorted(report) and report != sorted(report, reverse=True):
        return False

    # The distance deltas are all between 1 and 3
    if any(abs(y - x) < 1 or abs(y - x) > 3 for x, y in zip(report, report[1:])):
        return False

    return True

# PART 1
print(sum(1 for report in reports if is_safe(report)))

# Part 2
def is_dampened_safe(report):
    if is_safe(report):
        return True

    for i in range(len(report)):
        dampened = report[:i] + report[i+1:]
        if is_safe(dampened):
            return True

    return False

print(sum(1 for report in reports if is_dampened_safe(report)))
