from sys import stdin
from itertools import chain

lines = [line.strip() for line in stdin.readlines()]

to_ints = lambda xs: [int(x) for x in xs]
drawn_numbers = to_ints(lines[0].split(','))
boards = []

for line in lines[1:]:
    if line == '':
        boards.append([])
    else:
        boards[-1].append(to_ints(line.split()))

def rotate(lists):
    return list(zip(*lists))

def is_winner(choices, board):
    choices = set(choices)
    rows = map(set, board)
    cols = map(set, rotate(board))
    candidates = chain(rows, cols)

    for candidate in candidates:
        if candidate.issubset(choices):
            return True

    return False

def get_score(choices, board):
    numbers = set(chain(*board))

    unmarked_numbers = numbers - set(choices)
    most_recent_choice = choices[-1]

    return most_recent_choice * sum(unmarked_numbers)

def first_to_win(drawn_numbers, boards):
    choices = []
    for choice in drawn_numbers:
        choices.append(choice)

        for board in boards:
            if is_winner(choices, board):
                return (choices, board)

    return (choices, None)

def last_to_win(drawn_numbers, boards):
    choices = []
    winners = []

    for choice in drawn_numbers:
        choices.append(choice)

        current_winners = [board for board in boards if is_winner(choices, board)]
        current_losers = [board for board in boards if not is_winner(choices, board)]

        winners.extend((choices[:], winner) for winner in current_winners)
        boards = current_losers

    return winners[-1]

(choices, first_winner) = first_to_win(drawn_numbers, boards)
print(get_score(choices, first_winner))

(choices, last_winner) = last_to_win(drawn_numbers, boards)
print(get_score(choices, last_winner))
