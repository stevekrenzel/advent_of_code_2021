from sys import stdin

ROUNDS = [line.split() for line in stdin.read().splitlines()]

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

def score_round(theirs, mine):
    they_won = WIN_TO_LOSS[theirs] == mine
    they_lost = WIN_TO_LOSS[mine] == theirs

    points = 0 if they_won else 6 if they_lost else 3
    points_boost = SELECTION_POINT_BOOST[mine]

    return points + points_boost

# Part 1
total = sum(score_round(theirs, STATIC_MAP[mine]) for theirs, mine in ROUNDS)
print(total)

# Part 2
total = sum(score_round(theirs, DYNAMIC_MAP[mine](theirs)) for theirs, mine in ROUNDS)
print(total)
