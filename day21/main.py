from sys import stdin, exit
from itertools import product
from collections import Counter

lines = [line.strip() for line in stdin.readlines()]
player_positions = [int(line.split(': ')[1]) for line in lines]

def create_die(sides):
    counter = [0] # Boxed Int

    def roll():
        while True:
            for i in range(1, sides + 1):
                counter[0] = counter[0] + 1
                yield i

    return counter, roll()

def take_turn(player_position, die, board_size, rolls):
    move_amount = sum(next(die) for _ in range(rolls))
    new_position = ((player_position + move_amount - 1) % board_size) + 1
    return new_position

def play(player_positions, winning_score, board_size=10, rolls=3):
    count, die = create_die(100)
    scores = [0 for _ in player_positions]
    while True:
        for i, position in enumerate(player_positions):
            player_positions[i] = take_turn(position, die, board_size, rolls)
            scores[i] += player_positions[i]
            if scores[i] >= winning_score:
                return scores, count[0]

print(player_positions,)
scores, rolls = play(player_positions, 1000)
print(min(scores) * rolls)
