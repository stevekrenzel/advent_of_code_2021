from sys import stdin
from re import split
from typing import NamedTuple, Set

class ScratchCard(NamedTuple):
    id: int
    winning_numbers: Set[int]
    chosen_numbers: Set[int]

    def score(self) -> int:
        matches = self.matches()
        size = len(matches)
        if size == 0:
            return 0
        return 2 ** (size - 1)

    def matches(self) -> Set[int]:
        return self.winning_numbers.intersection(self.chosen_numbers)

    @staticmethod
    def from_string(s: str) -> 'ScratchCard':
        card_id_raw, numbers_raw = s.split(':')
        winning_numbers_raw, chosen_numbers_raw = numbers_raw.split('|')

        card_id = int(card_id_raw.strip().split(' ')[-1])
        winning_numbers = set(map(int, split(r'\s+', winning_numbers_raw.strip())))
        chosen_numbers = set(map(int, split(r'\s+', chosen_numbers_raw.strip())))

        return ScratchCard(card_id, winning_numbers, chosen_numbers)

class ScratchCardGroup(NamedTuple):
    cards: [ScratchCard]

    def total_instances(self) -> int:
        counts = {}
        cards = list(reversed(self.cards))

        for card in cards:
            size = len(card.matches())
            copy_range = range(1, size + 1)
            count = sum(counts.get(card.id + i, 0) for i in copy_range)
            counts[card.id] = 1 + count

        return sum(counts.values())

    @staticmethod
    def from_string(s: str) -> 'ScratchCardGroup':
        cards = list(map(ScratchCard.from_string, s.splitlines()))
        return ScratchCardGroup(cards)

lines = stdin.read()
group = ScratchCardGroup.from_string(lines)

# Part 1
print(sum(map(ScratchCard.score, group.cards)))

# Part 2
print(group.total_instances())
