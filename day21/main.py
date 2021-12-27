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
    player_positions = player_positions[:]
    scores = [0 for _ in player_positions]
    while True:
        for i, position in enumerate(player_positions):
            player_positions[i] = take_turn(position, die, board_size, rolls)
            scores[i] += player_positions[i]
            if scores[i] >= winning_score:
                return scores, count[0]

print(player_positions)
scores, rolls = play(player_positions, 1000)
print(min(scores) * rolls)

def quantum_play(player_positions, winning_score, player_scores=None, player_turn=0, board_size=10, rolls=3, memoized_results={}):
    if player_scores is None:
        player_scores = [0 for _ in player_positions]

    hashable_player_positions = tuple(p for p in player_positions)
    hashable_player_scores = tuple(s for s in player_scores)
    memoize_key = (hashable_player_positions, hashable_player_scores, player_turn)

    if memoize_key in memoized_results:
        return memoized_results[memoize_key]

    results = [0 for _ in player_positions]
    for player_index in range(len(player_positions)):
        if player_scores[player_index] >= winning_score:
            results[player_index] = 1
            return results

    all_roll_combinations = product(*[list(range(1,4)) for _ in range(rolls)])
    all_movement_amounts = map(sum, all_roll_combinations)
    movement_frequencies = Counter(all_movement_amounts)

    player_position = player_positions[player_turn]
    for move_amount, frequency in movement_frequencies.items():
        new_position = ((player_position + move_amount - 1) % board_size) + 1

        new_player_positions = player_positions[:]
        new_player_positions[player_turn] = new_position

        new_player_scores = player_scores[:]
        new_player_scores[player_turn] += new_position

        next_turn = (player_turn + 1) % len(player_positions)
        wins = quantum_play(new_player_positions, winning_score, new_player_scores, next_turn, board_size, rolls, memoized_results)

        results = [result + (count * frequency) for result, count in zip(results, wins)]

    memoized_results[memoize_key] = results
    return results

win_counts = quantum_play(player_positions, 21)
print(max(win_counts))
