from sys import stdin

lines = [line.strip() for line in stdin.readlines()]

depths = list(map(int, lines))
depth_pairs = zip(depths, depths[1:])
day_increases = sum(1 for (a, b) in depth_pairs if b > a)

windows = zip(depths, depths[1:], depths[2:])
window_sums = list(map(sum, windows))
window_pairs = zip(window_sums, window_sums[1:])
window_increases = sum(1 for (a, b) in window_pairs if b > a)

print(day_increases)
print(window_increases)
