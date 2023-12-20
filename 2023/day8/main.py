from sys import stdin
from itertools import cycle
from math import gcd

# Parsing input
lines = stdin.read().splitlines()
instructions = lines[0]

world = [line.split(' = ') for line in lines[2:]]
world = {parent: children[1:-1].split(', ') for parent, children in world}

# Helpers
lcm = lambda a, b: a * b // gcd(a, b)
DIRECTION = {'L': 0, 'R': 1}

# Both parts
parts = [
    {'AAA'}, # Part 1
    {node for node in world if node.endswith('A')}, # Part 2
]

for nodes in parts:
    distance = 1
    for count, movement in enumerate(cycle(instructions)):
        direction = DIRECTION[movement]
        nodes = [world[node][direction] for node in nodes]

        for node in nodes:
            if node.endswith('Z'):
                distance = lcm(distance, count + 1)
                nodes.remove(node)

        if len(nodes) == 0:
            break

    print(distance)
