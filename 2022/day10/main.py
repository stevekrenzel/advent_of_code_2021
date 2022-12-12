from sys import stdin
from typing import NamedTuple, Callable, Iterator

Registers = dict[str, int]

class CPU(NamedTuple):
    cycle: int = 1
    registers: Registers = {'x': 1}

    def set(self: 'CPU', register: str, value: int) -> 'CPU':
        # CPU is immutable, so we clone the registers
        registers = dict(self.registers.items())
        registers[register] = value

        return CPU(registers=registers, cycle=self.cycle)

    def get(self: 'CPU', register: str) -> int:
        return self.registers[register]

    def tick(self: 'CPU') -> 'CPU':
        return CPU(cycle=self.cycle + 1, registers=self.registers)

    def execute(self: 'CPU', instructions: list['Instruction']) -> Iterator['CPU']:
        cpu = self
        yield cpu

        for instruction in instructions:
            for cpu in instruction.execute(cpu):
                yield cpu

class OpCode(NamedTuple):
    name: str
    cycles: int
    execute: Callable[[CPU, list[int]], CPU]

class Instruction(NamedTuple):
    operation: OpCode
    args: list[int]

    def execute(self: 'Instruction', cpu: CPU) -> Iterator[CPU]:
        cycles = self.operation.cycles - 1
        for _ in range(cycles):
            cpu = cpu.tick()
            yield cpu

        cpu = cpu.tick()
        cpu = self.operation.execute(cpu, self.args)
        yield cpu

NOOP = OpCode('noop', 1, lambda cpu, _: cpu)
ADDX = OpCode('addx', 2, lambda cpu, args: cpu.set('x', cpu.get('x') + args[0]))
OP_CODES = {op.name:op for op in [NOOP, ADDX]}

def parse(line: str) -> Instruction:
    name, *args = line.split()
    operation = OP_CODES[name]
    return Instruction(operation, list(map(int, args)))

def signal_strength(cpus: Iterator[CPU], register: str, start: int, step: int) -> int:
    should_choose = lambda cpu: cpu.cycle >= start and (cpu.cycle - start) % step == 0
    chosen = filter(should_choose, cpus)
    return sum(cpu.cycle * cpu.get(register) for cpu in chosen)

def render(cpus: Iterator[CPU], register: str, screen_width: int) -> str:
    rows = []
    row = []

    for cpu in cpus:
        current_pixel = (cpu.cycle - 1) % screen_width
        sprite_position = cpu.get(register)

        is_active = abs(current_pixel - sprite_position) <= 1
        row.append('#' if is_active else '.')

        if cpu.cycle % screen_width == 0:
            rows.append(row)
            row = []

    if len(row) > 0:
        rows.append(row)

    return '\n'.join(''.join(row) for row in rows)


cpu = CPU()
operations = list(map(parse, stdin.read().splitlines()))

# Part 1
print(signal_strength(cpu.execute(operations), 'x', 20, 40))

# Part 2
print(render(cpu.execute(operations), 'x', 40))
