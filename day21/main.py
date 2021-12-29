from sys import stdin
from itertools import product
from functools import cache, reduce
from collections import namedtuple

Player = namedtuple('Player', ['position', 'score'])
Rules = namedtuple('Rules', ['die', 'winning_score', 'board_size', 'rolls_per_turn'], defaults=[10, 3])
GameState = namedtuple('GameState', ['players', 'turn', 'winner'], defaults=[0,None])
Game = namedtuple('Game', ['rules', 'state'])

lines = [line.strip() for line in stdin.readlines()]
players = tuple(Player(position=int(line.split(': ')[1]),score=0) for line in lines)

def roll(die, rolls):
    for combination in product(*(next(die) for _ in range(rolls))):
        yield sum(combination)

def move(player, spaces, board_size):
    position = ((player.position + spaces - 1) % board_size) + 1
    score = player.score + position
    return Player(position, score)

def find_winner(game):
    for player in game.state.players:
        if player.score >= game.rules.winning_score:
            return player

# A helper for setting an item in a tuple (which are immutable)
# We use tuples all over because they are hashable, and we need that to be able to use them as arguments in functions that use @cache
def set_item(i, tup, new_value):
    xs = list(tup)
    xs[i] = new_value
    return tuple(xs)

def next_turns(game):
    player_index = game.state.turn % len(game.state.players)
    player = game.state.players[player_index]

    for spaces in roll(game.rules.die, game.rules.rolls_per_turn):
        moved_player = move(player, spaces, game.rules.board_size)
        players = set_item(player_index, game.state.players, moved_player)
        state = game.state._replace(players=players, turn=game.state.turn + 1)
        yield Game(rules=game.rules, state=state)

@cache
def play(game, mapper, reducer):
    winner = find_winner(game)
    if winner is not None:
        state = game.state._replace(winner=winner)
        game = game._replace(state=state)
        return mapper(game)

    results = [play(next_turn, mapper, reducer) for next_turn in next_turns(game)]
    return reduce(reducer, results)

# ####################
# Deterministic
# ####################
def deterministic_die(sides):
    while True:
        for i in range(1, sides + 1):
            yield [i]

def score(game):
    turn = game.state.turn
    rolls = game.rules.rolls_per_turn
    min_score = min(player.score for player in game.state.players)
    return min_score * turn * rolls

def identity(_, score):
    return score

die = deterministic_die(100)
rules = Rules(die=deterministic_die(100), winning_score=1000)
state = GameState(players=players)
game = Game(rules=rules, state=state)

print(play(game, score, identity))

# ####################
# Quantum
# ####################
def quantum_die(sides):
    while True:
        yield list(range(1, sides + 1))

def wins(game):
    winner = game.state.winner
    players = game.state.players
    return [1 if winner == player else 0 for player in players]

def vector_addition(a, b):
    return [sum(pair) for pair in zip(a, b)]

rules = Rules(die=quantum_die(3), winning_score=21)
state = GameState(players=players)
game = Game(rules=rules, state=state)

print(max(play(game, wins, vector_addition)))
