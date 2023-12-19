from sys import stdin
from collections import Counter
from typing import NamedTuple

CHAR_TO_VAL = {
  'O': 0,
  '2': 2,
  '3': 3,
  '4': 4,
  '5': 5,
  '6': 6,
  '7': 7,
  '8': 8,
  '9': 9,
  'T': 10,
  'J': 11,
  'Q': 12,
  'K': 13,
  'A': 14,
}

HAND_TO_RANK = {
    (5,): 6, # Five of a kind
    (1, 4): 5, # Four of a kind
    (2, 3): 4, # Full house
    (1, 1, 3): 3, # Three of a kind
    (1, 2, 2): 2, # Two pairs
    (1, 1, 1, 2): 1, # One pair
    (1, 1, 1, 1, 1): 0, # High card
}

class Hand(NamedTuple):
  cards: [int]
  bid: int
  strength: int

  @staticmethod
  def parse(line: str, jokers: bool = False) -> 'Hand':
    cards_str, bid_str = line.split()
    cards_str = cards_str.replace('J', 'O') if jokers else cards_str
    cards = [CHAR_TO_VAL[c] for c in cards_str]
    bid = int(bid_str)
    return Hand(cards, bid, Hand.score(cards))

  @staticmethod
  def score(hand: [int]) -> int:
    jokers_count = hand.count(0)
    no_jokers = [card for card in hand if card != 0]

    counts = sorted(Counter(no_jokers).values()) if len(no_jokers) > 0 else [0]
    counts[-1] += jokers_count # Boost the most common card

    return HAND_TO_RANK[tuple(counts)]

# Parsing input
lines = stdin.readlines()
parsed = [
    [Hand.parse(line) for line in lines], # Part 1
    [Hand.parse(line, True) for line in lines], # Part 2
]

for hands in parsed:
    ordered = sorted(hands, key=lambda h: (h.strength, h.cards))
    ranked = [(rank + 1, hand) for rank, hand in enumerate(ordered)]
    score = sum(rank * hand.bid for rank, hand in ranked)
    print(score)
