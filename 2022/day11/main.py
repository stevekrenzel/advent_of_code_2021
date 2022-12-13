from enum import Enum, auto
from functools import reduce
from sys import stdin
from typing import NamedTuple, Callable

Item = int

class Operator(Enum):
    ADD = auto()
    MULTIPLY = auto()
    SQUARE = auto()

class Operation(NamedTuple):
    operator: Operator
    operand: int

    def eval(self: 'Operation', value: int):
        match self.operator:
            case Operator.ADD:
                return value + self.operand
            case Operator.MULTIPLY:
                return value * self.operand
            case Operator.SQUARE:
                return value * value
            case _:
                raise Exception(f"Unknown operator: {self.operator}")

    @staticmethod
    def parse(line: str) -> 'Operation':
        is_square = 'old * old' in line
        is_mult = '*' in line

        operator = Operator.SQUARE if is_square else Operator.MULTIPLY if is_mult else Operator.ADD
        operand = int(line.split()[-1]) if not is_square else 0

        return Operation(operator=operator, operand=operand)

class MonkeyTest(NamedTuple):
    modulus: int
    when_true: int
    when_false: int

    def eval(self: 'MonkeyTest', value: int):
        return self.when_true if (value % self.modulus) == 0 else self.when_false

    @staticmethod
    def parse(lines: list[str]) -> 'MonkeyTest':
        modulus = int(lines[0].split()[-1])
        when_true = int(lines[1].split()[-1])
        when_false = int(lines[2].split()[-1])

        return MonkeyTest(modulus=modulus, when_true=when_true, when_false=when_false)

WorryTransform = Callable[[int], int]

class Monkey:
    items: list[Item]
    operation: Operation
    test: MonkeyTest
    inspections: int = 0

    def __init__(self, items, operation, test):
        self.items = items
        self.operation = operation
        self.test = test

    def inspect(self: 'Monkey', monkies: list['Monkey'], worry_transform: WorryTransform):
        item = self.items.pop(0)
        self.inspections = self.inspections + 1

        worry_level = self.operation.eval(item)
        worry_level = worry_transform(worry_level)

        next_monkey = self.test.eval(worry_level)
        monkies[next_monkey].items.append(worry_level)

    @staticmethod
    def parse(lines: list[str]) -> 'Monkey':
        items = list(map(int, lines[1].split(': ')[1].split(', ')))
        operation = Operation.parse(lines[2])
        test = MonkeyTest.parse(lines[3:])
        return Monkey(items, operation, test)

def eval_round(monkies: list[Monkey], worry_transform: WorryTransform) -> list[Monkey]:
    monkies = monkies[:]

    for monkey in monkies:
        for _ in range(len(monkey.items)):
            monkey.inspect(monkies, worry_transform)

    return monkies

def eval(monkies: list[Monkey], rounds: int, worry_transform: WorryTransform) -> list[Monkey]:
    for _ in range(rounds):
        monkies = eval_round(monkies, worry_transform)
    return monkies

def parse(input: list[str]) -> list[Monkey]:
    monkies = []
    for i in range(0, len(input), 7):
        monkies.append(Monkey.parse(input[i : i + 6]))
    return monkies

def product(xs: list[int]) -> int:
    multiply = lambda a, b: a * b
    return reduce(multiply, xs, 1)


lines = stdin.read().splitlines()

# Part 1
transform = lambda worry_level: worry_level // 3
monkies = parse(lines)

part1_monkies = eval(monkies, 20, transform)
inspections = sorted([monkey.inspections for monkey in part1_monkies], reverse=True)
print(inspections[0] * inspections[1])

# Part 2
common_divisor = product([monkey.test.modulus for monkey in monkies])
transform = lambda worry_level: worry_level % common_divisor
monkies = parse(lines)

part2_monkies = eval(monkies, 10000, transform)
inspections = sorted([monkey.inspections for monkey in part2_monkies], reverse=True)
print(inspections[0] * inspections[1])
