from sys import stdin
from functools import reduce

def parse_round(round):
    parsed = [result.strip().split(' ') for result in round]
    return {color: int(count) for (count, color) in parsed}

def parse_rounds(rounds):
    return [parse_round(round) for round in rounds]

def parse_game(line):
    game_id, result = line.split(':')
    _, id = game_id.split(' ')
    matches = result.split(';')
    rounds = [match.split(',') for match in matches]
    return int(id), parse_rounds(rounds)

def are_viable(rounds, inventory):
    for round in rounds:
        for color, count in round.items():
            if color not in INVENTORY or count > INVENTORY[color]:
                return False
    return True

def minimum_set(rounds):
    colors = {}
    for round in rounds:
        for color, count in round.items():
            colors[color] = max(colors.get(color, 0), count)
    return colors

def power(min_set):
    mult = lambda x, y: x * y
    return reduce(mult, min_set.values())

INVENTORY = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

lines = stdin.readlines()
games = [parse_game(line) for line in lines]

# Part 1
viable_games = [id for (id, rounds) in games if are_viable(rounds, INVENTORY)]
print(sum(viable_games))

# Part 2
minimum_sets = [minimum_set(rounds) for (id, rounds) in games]
powers = [power(min_set) for min_set in minimum_sets]
print(sum(powers))
