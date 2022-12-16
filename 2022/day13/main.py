from sys import stdin
from functools import cmp_to_key

def cmp_int(left, right):
    return -1 if left < right else 0 if left == right else 1

def cmp(left, right):
    is_left_int = isinstance(left, int)
    is_right_int = isinstance(right, int)

    if is_left_int and is_right_int:
        return cmp_int(left, right)

    if is_right_int:
        return cmp(left, [right])

    if is_left_int:
        return cmp([left], right)

    orderings = (cmp(l, r) for l, r in zip(left, right))
    for ordering in orderings:
        if ordering != 0:
            return ordering

    return cmp(len(left), len(right))

packets = [eval(line) for line in stdin.read().splitlines() if line != ""]
pairs = list(zip(packets[0::2], packets[1::2]))

# Part 1
print(sum(i + 1 for i, (a, b) in enumerate(pairs) if cmp(a, b) <= 0))

# Part 2
dividers = [[[2]], [[6]]]
packets = packets + dividers

ordered = sorted(packets, key=cmp_to_key(cmp))
indexes = [ordered.index(divider) + 1 for divider in dividers]

print(indexes[0] * indexes[1])
