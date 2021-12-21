from sys import stdin
from math import floor, ceil

class Box:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

# Wrap every list and element in a box for easy manipulation via references
def box(xs):
    if type(xs) != list:
        return Box(xs)
    return Box(list(map(box, xs)))

def add(x, y):
    added = Box([x, y])
    reduce(added)
    return added

def walk_tree(tree, depth=0, parent=None):
    yield tree, depth, parent

    if type(tree.value) != list:
        return

    for node in tree.value:
        yield from walk_tree(node, depth+1, tree)

def enum_leaves(tree):
    for leaf, _, parent in walk_tree(tree):
        if type(leaf.value) != list:
            yield leaf, parent

def nearest_left_leaf(node, tree):
    leaves = list(enum_leaves(tree))
    pairs = zip(leaves, leaves[1:])

    for (left_leaf, _), (_, right_parent) in pairs:
        if right_parent == node:
            return left_leaf

def nearest_right_leaf(node, tree):
    leaves = list(reversed(list(enum_leaves(tree))))
    pairs = zip(leaves, leaves[1:])

    for (left_leaf, _), (_, right_parent) in pairs:
        if right_parent == node:
            return left_leaf

def first_deep_pair(tree):
    for leaf, depth, _ in walk_tree(tree):
        if depth == 4 and type(leaf.value) == list:
            return leaf

def first_large_leaf(tree):
    for leaf, _ in enum_leaves(tree):
        if leaf.value >= 10:
            return leaf

def explode(node, tree):
    left, right = node.value

    nearest_left = nearest_left_leaf(node, tree)
    if nearest_left is not None:
        nearest_left.value = nearest_left.value + left.value

    nearest_right = nearest_right_leaf(node, tree)
    if nearest_right is not None:
        nearest_right.value = nearest_right.value + right.value

    node.value = 0

def split(node):
    left = int(floor(node.value / 2))
    right = int(ceil(node.value / 2))
    node.value = [box(left), box(right)]

def reduce(tree):
    deep_pair = first_deep_pair(tree)
    if deep_pair is not None:
        explode(deep_pair, tree)
        reduce(tree)

    large_leaf = first_large_leaf(tree)
    if large_leaf is not None:
        split(large_leaf)
        reduce(tree)

def magnitude(tree):
    if type(tree.value) != list:
        return tree.value

    left, right = tree.value
    return (magnitude(left) * 3) + (magnitude(right) * 2)

def total_sum(trees):
    total = None
    for tree in trees:
        if total is None:
            total = tree
        else:
            total = add(total, tree)
    return total

lines = [line.strip() for line in stdin.readlines()]
snailfish_numbers = [box(eval(line)) for line in lines] # Forgive me for using `eval` on arbitrary input

total = total_sum(snailfish_numbers)
print(magnitude(total))

cross_product = (add(box(eval(line1)), box(eval(line2))) for i, line1 in enumerate(lines) for j, line2 in enumerate(lines) if i != j)
print(magnitude(max(cross_product, key=magnitude)))
