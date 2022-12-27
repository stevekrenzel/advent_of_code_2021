from sys import stdin
from itertools import cycle
from enum import Enum, auto
from typing import Iterable
from dataclasses import dataclass, field

Point = tuple[int, int]
Shape = set[Point]

class Command(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()

    @staticmethod
    def parse(char: str) -> 'Command':
        return Command.LEFT if char == '<' else Command.RIGHT

    def apply(self: 'Command', shape: Shape) -> Shape:
        xd = {Command.LEFT: -1, Command.RIGHT: 1, Command.DOWN: 0}[self]
        yd = {Command.LEFT: 0, Command.RIGHT: 0, Command.DOWN: -1}[self]
        return shift(shape, xd, yd)

@dataclass
class Chamber:
    points: set[Point] = field(default_factory=set)
    height: int = 0
    width: int = 7
    total_shapes_added: int = 0
    signatures: dict[str, tuple[int, int]] = field(default_factory=dict)

    def add_shapes(self: 'Chamber', count: int, shapes: Iterable[Shape], commands: Iterable[Command], analyze_cycles: bool = True):
        for shape in take(count, shapes):
            self.add_shape(shape, commands)

            if not analyze_cycles:
                continue

            signature = self.get_signature()
            if signature in self.signatures:
                adjustment, remainder = self.get_height_adjustment(signature, count)
                self.add_shapes(remainder, shapes, commands, False)
                self.height += adjustment
                return
            self.signatures[signature] = (self.total_shapes_added, self.height)

    def add_shape(self: 'Chamber', shape: Shape, commands: Iterable[Command], offset: Point = (3, 4)):
        shape = shift(shape, offset[0], self.height + offset[1])

        for command in commands:
            # Move left or right
            shape, finished = self.process_command(command, shape)
            if finished:
                break

            # Then move down
            shape, finished = self.process_command(Command.DOWN, shape)
            if finished:
                break

        self.total_shapes_added += 1

    def get_height_adjustment(self: 'Chamber', signature: str, total: int) -> tuple[int, int]:
        previous_count, previous_height = self.signatures[signature]

        remaining_shapes = total - self.total_shapes_added
        shapes_in_cycle = self.total_shapes_added - previous_count
        cycle_height = self.height - previous_height

        quotient, remainder = divmod(remaining_shapes, shapes_in_cycle)
        return (quotient * cycle_height, remainder)


    def intersects(self: 'Chamber', shape: Shape) -> bool:
        left, right = min(x for x, _ in shape), max(x for x, _ in shape)

        touched_wall = left <= 0 or right >= self.width + 1
        touched_floor = any(y <= 0 for _, y in shape)
        touched_rock = len(self.points & shape) > 0

        return touched_wall or touched_floor or touched_rock

    def get_signature(self: 'Chamber') -> str:
        # Assume that looking back 64 rows is sufficient for a distinct signature
        coords = [(x, y) for x in range(1, self.width + 1) for y in range(self.height - 64, self.height + 1)]

        # Convert cells to a binary string
        return ''.join('1' if point in self.points else '0' for point in coords)

    def process_command(self: 'Chamber', command: Command, shape: Shape) -> tuple[Shape, bool]:
        moved_shape = command.apply(shape)
        touches = self.intersects(moved_shape)

        # If we intersect anything, keep the unmoved version of the shape
        new_shape = shape if touches else moved_shape

        # If we move down and hit something, stop processing commands
        stop_processing = touches and command == Command.DOWN

        # Update the new chamber height
        if stop_processing:
            height = max(self.height, max(y for _, y in shape))
            self.points.update(shape)
            self.height = height

        return (new_shape, stop_processing)

def shift(shape: Shape, xd: int, yd: int) -> Shape:
    return set((x + xd, y + yd) for x, y in shape)

def take(n, iterator):
    return (next(iterator) for _ in range(n))

SHAPES = [
    {(1,0), (2,0), (3,0), (0,0)},        # –
    {(0,1), (1,2), (2,1), (1,1), (1,0)}, # +
    {(0,0), (1,0), (2,0), (2,1), (2,2)}, # ⅃
    {(0,1), (0,2), (0,3), (0,0)},        # |
    {(1,0), (0,1), (1,1), (0,0)},        # ■
]

COMMANDS = [Command.parse(char) for char in stdin.read().strip()]

# Part 1
chamber = Chamber()
shapes = cycle(SHAPES)
commands = cycle(COMMANDS)
chamber.add_shapes(2022, shapes, commands)
print(chamber.height)

# Part 2
chamber = Chamber()
shapes = cycle(SHAPES)
commands = cycle(COMMANDS)
chamber.add_shapes(1000000000000, shapes, commands)
print(chamber.height)
