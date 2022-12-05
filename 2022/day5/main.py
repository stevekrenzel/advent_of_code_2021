from sys import stdin
from typing import NamedTuple

class MoveCommand(NamedTuple):
    quantity: int
    starting_stack: int
    ending_stack: int

def parse_input(lines):
    # Find the break in the file between stack descriptions and move commands
    end_of_stack_description = lines.index("")

    raw_stack_description = lines[:end_of_stack_description]
    raw_move_commands = lines[end_of_stack_description + 1:]

    stack_description = parse_stack_description(raw_stack_description)
    move_commands = parse_move_commands(raw_move_commands)

    return (stack_description, move_commands)

def parse_stack_description(lines):
    # We don't need the last line of the description. It's just numbers.
    lines = lines[:-1]

    # Start from the bottom of the lines and work up.
    descriptions = reversed(lines)

    # Parse each level of crates and get a list of each level
    levels = map(parse_crate_description, descriptions)

    # We rotate the levels (matrix rotation) to get from levels to stacks
    # [[None, A, None],    [[B, D   , None],
    #  [B   , C, None], =>  [E, C   , A   ],
    #  [D   , E, F   ]]     [F, None, None]]
    rotated = zip(*levels)

    # Filter None values from the stacks and return them
    is_defined = lambda x: x is not None
    stacks = [list(filter(is_defined, stack)) for stack in rotated]
    return stacks

def parse_crate_description(line):
    raw_crates = [line[i:i + 3].strip() for i in range(0, len(line), 4)]

    # If a crate is defined, it'll have a value like `[A]`, so we take `crate[1]` to get the letter
    crates = [crate[1] if len(crate) > 0 else None for crate in raw_crates]
    return crates

def parse_move_commands(lines):
    # Lines are of the form "move 3 from 5 to 7". Fortunately, that
    # means we can `split` on whitespace and take the odd indices from
    # the split.
    parsed_lines = [line.split()[1::2] for line in lines]

    commands = [MoveCommand(int(quantity), int(start), int(end)) for quantity, start, end in parsed_lines]
    return commands

def evaluate_commands(commands, stacks, move_strategy):
     # We clone the stacks so we don't mutate the originals
    stacks = [stack[:] for stack in stacks]

    for quantity, starting_stack, ending_stack in commands:
        start, end = stacks[starting_stack - 1], stacks[ending_stack - 1]

        # Note: `move_strategy` is expected to mutate the `start` stack.
        end.extend(move_strategy(quantity, start))

    return stacks

def read_tops(stacks):
    return ''.join(stack[-1] for stack in stacks)

lines = stdin.read().splitlines()
stacks, commands = parse_input(lines)

# Part 1
move_strategy = lambda quantity, stack: [stack.pop() for _ in range(quantity)]
new_stacks = evaluate_commands(commands, stacks, move_strategy)
print(read_tops(new_stacks))

# Part 2
move_strategy = lambda quantity, stack: reversed([stack.pop() for _ in range(quantity)])
new_stacks = evaluate_commands(commands, stacks, move_strategy)
print(read_tops(new_stacks))
