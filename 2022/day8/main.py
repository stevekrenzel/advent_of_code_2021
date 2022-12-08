from sys import stdin
from enum import Enum, auto
from math import prod
from typing import NamedTuple, Iterator

class Position(NamedTuple):
    x: int
    y: int


class Tree(NamedTuple):
    position: Position
    height: int

TreeGrid = list[list[Tree]]

class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

DIRECTION_DELTA = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}

lines: list[str] = stdin.read().splitlines()
trees: TreeGrid = [[Tree(Position(x, y), int(height)) for x, height in enumerate(line)] for y, line in enumerate(lines)]

def iter_tree_line(start: Tree, looking: Direction, trees: TreeGrid) -> Iterator[Tree]:
    """ Iterates through the trees in a given line in the grid. """
    if len(trees) == 0:
        return

    dx, dy = DIRECTION_DELTA[looking]
    width, height = len(trees[0]), len(trees)
    x, y = start.position.x, start.position.y

    while x >= 0 and x < width and y >= 0 and y < height:
        yield trees[y][x]
        x, y = x + dx, y + dy

def visible_trees(start: Tree, looking: Direction, trees: TreeGrid) -> Iterator[Tree]:
    """ Returns the set of visible trees from a given tree and direction. """
    heighest = None
    for tree in iter_tree_line(start, looking, trees):
        if heighest is None or tree.height > heighest.height:
            yield tree
            heighest = tree

def externally_visible_trees(grid: TreeGrid) -> Iterator[Tree]:
    """ Returns trees that are visible from positions outside of the grid.

    The same tree may be returned multiple times if visible from multiple positions.
    """
    if len(grid) == 0:
        return 0

    top = (grid[0], Direction.SOUTH)
    bottom = (grid[-1], Direction.NORTH)
    left = ([row[0] for row in grid], Direction.EAST)
    right = ([row[-1] for row in grid], Direction.WEST)

    for trees, direction in [top, bottom, left, right]:
        for tree in trees:
            yield from visible_trees(tree, direction, grid)

def viewing_distance(tree: Tree, looking: Direction, trees: TreeGrid) -> int:
    dist = 0
    for dist, candidate in enumerate(iter_tree_line(tree, looking, trees)):
        if dist > 0 and candidate.height >= tree.height:
            break
    return dist

def scenic_score(tree: Tree, grid: TreeGrid) -> int:
    return prod(viewing_distance(tree, direction, grid) for direction in Direction)

# Part 1
print(len(set(externally_visible_trees(trees))))

# Part 2
print(max(scenic_score(tree, trees) for row in trees for tree in row))
