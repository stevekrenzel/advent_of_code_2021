from sys import stdin
from enum import IntEnum

ROUNDS = [line.split() for line in stdin.read().splitlines()]

# Possible outcomes of a round, with their values being points awarded for each
class Outcome(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0

# Maps a winning choice to its losing counterpart
WIN_TO_LOSS = {
    'B': 'A',
    'C': 'B',
    'A': 'C',
}

# Maps a losing choice to its winning counterpart
LOSS_TO_WIN = {val:key for key, val in WIN_TO_LOSS.items()}

# The selection that is played impacts the total score of the round
SELECTION_POINT_BOOST = {
    'A': 1,
    'B': 2,
    'C': 3,
}

# Part 1 maps codes to static values
STATIC_MAP = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
}

# Part 2 maps codes dynamically depending on the other choice
DYNAMIC_MAP = {
    'X': lambda their_choice: WIN_TO_LOSS[their_choice], # Force a loss
    'Y': lambda their_choice: their_choice, # Force a draw
    'Z': lambda their_choice: LOSS_TO_WIN[their_choice], # Force a win
}

def round_outcome(theirs, mine):
    if WIN_TO_LOSS[theirs] == mine:
        return Outcome.LOSS

    if WIN_TO_LOSS[mine] == theirs:
        return Outcome.WIN

    return Outcome.DRAW

def score_round(theirs, mine):
    points = round_outcome(theirs, mine)
    points_boost = SELECTION_POINT_BOOST[mine]

    return points + points_boost

# Part 1
total = sum(score_round(theirs, STATIC_MAP[mine]) for theirs, mine in ROUNDS)
print(total)

# Part 2
total = sum(score_round(theirs, DYNAMIC_MAP[mine](theirs)) for theirs, mine in ROUNDS)
print(total)
