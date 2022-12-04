from sys import stdin

def parse_range(text):
    pair = text.split('-')
    return tuple(map(int, pair))

def is_subset(range1, range2):
    """ Returns True if `range2` is subset of `range1`. """
    lower1, upper1 = range1
    lower2, upper2 = range2
    return lower1 <= lower2 and upper1 >= upper2

def is_redundant(range1, range2):
    """ Returns True if either range is fully contained in the other. """
    return is_subset(range1, range2) or is_subset(range2, range1)

def is_overlapping(range1, range2):
    """ Returns True if `range1` and `range2` have any overlap. """
    lower1, upper1 = range1
    lower2, upper2 = range2
    return upper1 >= lower2 and upper2 >= lower1

lines = stdin.read().splitlines()
pairs = [line.split(',') for line in lines]
assignments = [(parse_range(elf1), parse_range(elf2)) for elf1, elf2, in pairs]

# Part 1
print(sum(1 for elf1, elf2 in assignments if is_redundant(elf1, elf2)))

# Part 2
print(sum(1 for elf1, elf2 in assignments if is_overlapping(elf1, elf2)))
