from sys import stdin
from typing import NamedTuple, Set
from string import digits

class Coordinate(NamedTuple):
    x: int
    y: int

    def neighboring_coordinates(self):
        return {
            Coordinate(self.x + xd, self.y + yd)
            for xd in [-1, 0, 1]
            for yd in [-1, 0, 1]
            if xd != 0 or yd != 0
        }

    def is_neighbor(self, other):
        return len(other.neighboring_coordinates() & {self}) > 0

class Range(NamedTuple):
    coordinates: Set[Coordinate]

    def add_coordinate(self, coordinate):
        return Range(self.coordinates | {coordinate})

    def neighboring_coordinates(self):
        return {
            neighbor
            for coordinate in self.coordinates
            for neighbor in coordinate.neighboring_coordinates()
        }

    def is_neighbor(self, other):
        return len(other.neighboring_coordinates() & self.coordinates) > 0

class GridCell(NamedTuple):
    value: str
    coordinate: Coordinate

    def is_digit(self):
        return self.value in digits

    def is_blank_space(self):
        return self.value == '.'

    def is_symbol(self):
        return not (self.is_digit() or self.is_blank_space())

class Grid(NamedTuple):
    grid: [[GridCell]]

    @staticmethod
    def from_string(raw_string):
        grid = [[
            GridCell(c, Coordinate(x, y))
            for x, c in enumerate(line)
        ] for y, line in enumerate(raw_string.splitlines())]
        return Grid(grid)

    def symbols(self):
        return [
            cell
            for row in self.grid
            for cell in row
            if cell.is_symbol()
        ]

    def numbers(self):
        numbers = []

        is_not_digit = lambda cell: not cell.is_digit()
        seek_digit = lambda cells: drop_while(is_not_digit, cells)

        is_digit = lambda cell: cell.is_digit()
        pop_digits = lambda cells: take_while(is_digit, seek_digit(cells))

        for row in self.grid:
            cells = row[:]
            while len(cells) > 0:
                digits, cells = pop_digits(cells)
                number = Number.from_cells(digits)
                if not number:
                    break
                numbers.append(number)
        return numbers

    def part_numbers(self):
        return [
            number
            for number in self.numbers()
            if number.is_part_number(self)
        ]

    def gears(self):
        candidates = [symbol for symbol in self.symbols() if symbol.value == '*']
        part_numbers = self.part_numbers()
        gears = []
        for candidate in candidates:
            neighboring_parts = [
                part_number
                for part_number in part_numbers
                if part_number.coordinates.is_neighbor(candidate.coordinate)
            ]
            if len(neighboring_parts) == 2:
                gears.append(Gear(tuple(neighboring_parts), candidate.coordinate))
        return gears

class Number(NamedTuple):
    value: int
    coordinates: Range

    def add_cell(self, cell):
        new_value = (self.value * 10) + int(cell.value)
        new_coordinates = self.coordinates.add_coordinate(cell.coordinate)
        return Number(new_value, new_coordinates)

    def is_part_number(self, world):
        symbol_coordinates = Range({s.coordinate for s in world.symbols()})
        return self.coordinates.is_neighbor(symbol_coordinates)

    @staticmethod
    def from_cell(cell):
        return Number(int(cell.value), Range({cell.coordinate}))

    @staticmethod
    def from_cells(cells):
        if len(cells) == 0:
            return None
        number = Number.from_cell(cells.pop(0))
        for cell in cells:
            number = number.add_cell(cell)
        return number

class Symbol(NamedTuple):
    value: str
    coordinate: Coordinate

    def neighboring_parts(self, world):
        part_numbers = world.part_numbers()
        return [
            part_number
            for part_number in part_numbers
            if part_number.coordinates.is_neighbor(self.coordinate)
        ]

    @staticmethod
    def from_cell(cell):
        return Symbol(cell.value, cell.coordinate)

class Gear(NamedTuple):
    part_numbers: tuple[Number, Number]
    coordinate: Coordinate

    def ratio(self):
        (p1, p2) = self.part_numbers
        return p1.value * p2.value

# Helpers for consuming from token streams
def drop_while(predicate, iterable):
    iterable = iterable[:]
    while len(iterable) > 0:
        if not predicate(iterable[0]):
            break
        iterable.pop(0)
    return iterable

def take_while(predicate, iterable):
    iterable = iterable[:]
    result = []
    while len(iterable) > 0:
        if not predicate(iterable[0]):
            break
        result.append(iterable.pop(0))
    return result, iterable

lines = stdin.read()
world = Grid.from_string(lines)

# Part 1
print(sum(p.value for p in world.part_numbers()))

# Part 2
print(sum(g.ratio() for g in world.gears()))
