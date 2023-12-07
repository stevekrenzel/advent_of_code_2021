from sys import stdin
from math import sqrt, ceil, floor
from functools import reduce

def winning_combinations(race):
    max_time, best_distance = race

    shared = sqrt((max_time ** 2) - (4 * best_distance))
    lower = floor(((max_time - shared) / 2) + 1)
    upper = ceil(((max_time + shared) / 2) - 1)

    return upper - lower + 1

def product(xs):
    return reduce(lambda x, y: x * y, xs)

# Parsing input
lines = stdin.readlines()

raw_times = [time for time in lines[0].split(':')[1].strip().split(' ') if len(time.strip()) > 0]
raw_distances = [distance for distance in lines[1].split(':')[1].strip().split(' ') if len(distance.strip()) > 0]

# Part 1
times = [int(token) for token in raw_times]
distances = [int(token) for token in raw_distances]
races = zip(times, distances)

print(product(winning_combinations(race) for race in races))

# Part 2
time = int(''.join(raw_times))
distance = int(''.join(raw_distances))
race = (time, distance)

print(winning_combinations(race))
