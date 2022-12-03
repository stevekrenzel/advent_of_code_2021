from sys import stdin
from string import ascii_lowercase, ascii_uppercase
from functools import reduce

# Some type aliases to improve clarity
Item = str
Compartment = set[Item]
Rucksack = tuple[Compartment, Compartment]

def line_to_rucksack(line: str) -> Rucksack:
    """ Converts a line to a rucksack. """

    midpoint = len(line) // 2
    left_compartment, right_compartment = line[:midpoint], line[midpoint:]

    return (set(left_compartment), set(right_compartment))

def common_items(rucksack: Rucksack) -> set[Item]:
    """ Returns any items that are in both compartments of a rucksack. """

    return rucksack[0] & rucksack[1]

def priority(item: Item) -> int:
    """ Returns an item's priority. """

    if item in ascii_lowercase:
        return ascii_lowercase.index(item) + 1

    return ascii_uppercase.index(item) + 27

def group(items, size):
    """
    Splits a list into sublists of length `size`.
    The last sublist may be smaller.

    Example:
    >>> group([1,2,3,4,5,6,7,8], 3)
    [[1,2,3],[4,5,6],[7,8]]
    """

    groups = []

    for i in range(0, len(items), size):
        groups.append(items[i : i + size])

    return groups

def intersect(rucksacks: list[Rucksack]) -> set[Item]:
    """ Intersects the complete contents of multiple rucksacks together. """

    # Union the compartments of each rucksack, because each rucksack has two compartments
    unioned = [left | right for left, right in rucksacks]

    # Intersect them all together
    intersect = lambda a, b: a & b
    return reduce(intersect, unioned)

lines = stdin.read().splitlines()
rucksacks = [line_to_rucksack(line) for line in lines]

# Part 1
common = map(common_items, rucksacks)
priorities = (priority(item) for items in common for item in items)

print(sum(priorities))

# Part 2
ELVES_PER_GROUP = 3

groups = group(rucksacks, ELVES_PER_GROUP)
common = map(intersect, groups)
priorities = (priority(item) for items in common for item in items)

print(sum(priorities))
