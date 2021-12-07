from sys import stdin
from operator import ge, lt

lines = [line.strip() for line in stdin.readlines()]

def rotate(lists):
    return list(zip(*lists))

def gamma_and_epsilon(lines):
    gamma = 0
    epsilon = 0

    for row in rotate(lines):
        # Shift existing values
        gamma *= 2
        epsilon *= 2

        if row.count('1') > row.count('0'):
            gamma += 1
        else:
            epsilon += 1

    return (gamma, epsilon)

def rating_filter(candidates, cmp):
    if len(candidates) == 0:
        raise Exception("There weren't any candidates provided")

    for i in range(len(candidates[0])):
        row = rotate(candidates)[i]

        one_count = row.count('1')
        zero_count = row.count('0')
        keeper = '0' if one_count == 0 else \
                 '1' if zero_count == 0 else \
                 '1' if cmp(one_count, zero_count) else \
                 '0'

        candidates = [candidate for candidate in candidates if candidate[i] == keeper]

    if len(candidates) > 1:
        raise Exception("Too many candidates")

    if len(candidates) == 0:
        raise Exception("No candidates were found")

    return int(candidates[0], 2)

def oxygen_rating(candidates):
    return rating_filter(candidates, ge)

def co2_rating(candidates):
    return rating_filter(candidates, lt)

(gamma, epsilon) = gamma_and_epsilon(lines)
print(gamma * epsilon)

oxygen = oxygen_rating(lines)
co2 = co2_rating(lines)
print(oxygen * co2)
