from sys import stdin

lines = [line.strip().split() for line in stdin.readlines()]
commands = [(command, int(distance)) for (command, distance) in lines]

def explore(commands):
    depth = 0
    horizontal = 0

    for (command, distance) in commands:
        if command == 'forward':
            horizontal += distance
        elif command == 'down':
            depth += distance
        elif command == 'up':
            depth -= distance
        else:
            raise Exception("Unknown command: " + command)

    return (horizontal, depth)

def explore_and_aim(commands):
    depth = 0
    horizontal = 0
    aim = 0

    for (command, distance) in commands:
        if command == 'forward':
            horizontal += distance
            depth += (aim * distance)
        elif command == 'down':
            aim += distance
        elif command == 'up':
            aim -= distance
        else:
            raise Exception("Unknown command: " + command)

    return (horizontal, depth, aim)

(horizontal, depth) = explore(commands)
print(horizontal * depth)

(horizontal, depth, _) = explore_and_aim(commands)
print(horizontal * depth)
