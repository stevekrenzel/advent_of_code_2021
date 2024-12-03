from sys import stdin
import re

# Read the input as a single string, including all lines
raw_input = stdin.read()

def evaluate_command(command):
    x, y = command
    return x * y

def evaluate_commands(commands):
    return [evaluate_command(command) for command in commands]

# PART 1
def extract_commands(raw_input):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    return [(int(x), int(y)) for x, y in re.findall(pattern, raw_input)]

commands = extract_commands(raw_input)
evaluated = evaluate_commands(commands)
print(sum(evaluated))

# PART 2

# Note: Most problems in AoC operate per line, but this program
# requires tracking the do/don't state across multiple lines.
# That's why we never split on lines.
def extract_conditional_commands(raw_input):
    commands = []
    pattern = r"(mul)\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))"
    include = True

    matches = re.findall(pattern, raw_input)
    for (command, x, y, do, dont) in matches:
        if include and command == "mul":
            commands.append((int(x), int(y)))
        if do:
            include = True
        if dont:
            include = False

    return commands

commands = extract_conditional_commands(raw_input)
evaluated = evaluate_commands(commands)
print(sum(evaluated))
