from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import Iterator, NamedTuple

class Position(NamedTuple):
    x: int
    y: int

    def __add__(self: 'Position', vector: 'Vector') -> 'Position':
        return Position(self.x + vector.dx, self.y + vector.dy)

    def chebyshev_distance(self: 'Position', other: 'Position') -> int:
        return max([abs(self.x - other.x), abs(self.y - other.y)])

class Vector(NamedTuple):
    dx: int
    dy: int

class Rope(NamedTuple):
    knots: list[Position]

    @staticmethod
    def new(knot_count: int) -> 'Rope':
        """ Creates a new rope of length `knot_count` """
        return Rope([Position(0, 0) for _ in range(knot_count)])

    def move(self: 'Rope', movement: 'Movement') -> Iterator['Rope']:
        """ Moves a rope and yields a new rope for each intermediate step. """
        direction, distance = movement
        rope: 'Rope' = self

        yield rope
        for _ in range(distance):
            rope = rope.move_once(direction)
            yield rope

    def move_once(self: 'Rope', direction: 'Direction') -> 'Rope':
        """ Moves the head of a rope one square, and adjusts the rest of the rope. """
        previous_head = self.knots[0]

        new_head = previous_head + direction.vector()
        knots =[new_head]

        for knot in self.knots[1:]:
            previous = knots[-1]
            too_long = previous.chebyshev_distance(knot) > 1

            x_adjustment = 0 if not too_long else cmp(previous.x, knot.x)
            y_adjustment = 0 if not too_long else cmp(previous.y, knot.y)
            adjustment = Vector(x_adjustment, y_adjustment)

            new_knot = knot + adjustment
            knots.append(new_knot)

        return Rope(knots)

class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()

    def vector(self: 'Direction') -> Vector:
        return {
            Direction.RIGHT: Vector(1, 0),
            Direction.LEFT: Vector(-1, 0),
            Direction.UP: Vector(0, 1),
            Direction.DOWN: Vector(0, -1),
        }[self]

    @staticmethod
    def from_character(character: str) -> 'Direction':
        return {
            'R': Direction.RIGHT,
            'L': Direction.LEFT,
            'U': Direction.UP,
            'D': Direction.DOWN
        }[character]

class Movement(NamedTuple):
    direction: Direction
    distance: int

    @staticmethod
    def parse(text: str) -> 'Movement':
        components = text.split()
        direction, distance = Direction.from_character(components[0]), int(components[1])
        return Movement(direction, distance)

def cmp(a:int, b:int) -> int:
    return -1 if (a < b) else 1 if (a > b) else 0

def run_movements(rope: Rope, movements: list[Movement]) -> Iterator[Rope]:
    # We reuse `rope` as the loop variable so every new movement uses the previously yielded rope.
    for movement in movements:
        for rope in rope.move(movement):
            yield rope

movements: list[Movement] = [Movement.parse(line) for line in stdin.read().splitlines()]

# Part 1
rope = Rope.new(2)
print(len(set(rope.knots[-1] for rope in run_movements(rope, movements))))

# Part 2
rope = Rope.new(10)
print(len(set(rope.knots[-1] for rope in run_movements(rope, movements))))
