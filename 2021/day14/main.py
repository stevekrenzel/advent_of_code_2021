from sys import stdin
from collections import Counter

lines = [line.strip() for line in stdin.readlines()]

template = lines[0]
substitutions = {(key[0], key[1]): val for key, val in (line.split(' -> ') for line in lines[2:])}

def pairs(polymer):
    polymer = [None] + list(polymer) + [None]
    return zip(polymer, polymer[1:])

def to_counted_polymer(template):
    return Counter(pairs(template))

def substitute(polymer, substitutions):
    substituted = polymer.copy()
    items = list(substituted.items())

    for (a, b), counts in items:
        if (a, b) in substitutions:
            substitution = substitutions[(a, b)]

            substituted.subtract({(a, b): counts})
            substituted.update({(a, substitution): counts})
            substituted.update({(substitution, b): counts})

            if substituted[(a, b)] == 0:
                del substituted[(a, b)]

    return substituted

def repeated_substitution(template, substitutions, iterations):
    for _ in range(iterations):
        template = substitute(template, substitutions)
    return template

def count_elements(polymer):
    counted = Counter()

    for (a, b), counts in polymer.items():
        counted.update({a: counts})
        counted.update({b: counts})

    deduped = Counter({a: count // 2 for a, count in counted.items() if a is not None})
    return deduped

def polymer_length(polymer):
    return sum(count_elements(polymer).values())

def most_common_element(polymer):
    counts = count_elements(polymer)
    return counts.most_common(1)[0]

def least_common_element(polymer):
    counts = count_elements(polymer)
    return counts.most_common()[-1]

def max_delta(polymer):
    most_common = most_common_element(substituted)[1]
    least_common = least_common_element(substituted)[1]
    return most_common - least_common

polymer = to_counted_polymer(template)
for count in [10, 40]:
    substituted = repeated_substitution(polymer, substitutions, count)
    delta = max_delta(substituted)
    print(delta)
