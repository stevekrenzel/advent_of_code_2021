from sys import stdin
from collections import Counter

# Raw lines from input
lines = stdin.readlines()

# Split each line into a pair of strings
# (e.g. ["1 2", "3 4"] -> [["1", "2"], ["3", "4"]])
pairs = [line.strip().split() for line in lines]

# Transpose each row into columns
# (e.g. [["1", "2"], ["3", "4"]] -> [["1", "3"], ["2", "4"]])
columns = list(zip(*pairs))

# Convert each column into a list of integers
# (e.g. [["1", "3"], ["2", "4"]] -> [[1, 3], [2, 4]])
ints = [[int(x) for x in c] for c in columns]

# Sort each list of integers
# (e.g. [[1, 3], [2, 4]] -> [[1, 3], [2, 4]])
ordered = [sorted(c) for c in ints]

# Calculate the distance between each pair of integers
# (e.g. [[1, 3], [2, 4]] -> [2, 2])
distances = [abs(x - y) for x, y in zip(*ordered)]

# PART 1

# Sum up all of the distances
# (e.g. [2, 2] -> 4)
print(sum(distances))

# PART 2

(xs, ys) = ordered
counts = Counter(ys)

similarity = sum(x * counts[x] for x in xs)
print(similarity)
