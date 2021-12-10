from sys import stdin
from math import prod

lines = [line.strip() for line in stdin.readlines()]

PAIRS = {
    '{': '}',
    '(': ')',
    '[': ']',
    '<': '>',
}

ERROR_POINTS = {
    '}': 1197,
    ')': 3,
    ']': 57,
    '>': 25137,
}

INCOMPLETE_POINTS = {
    '}': 3,
    ')': 1,
    ']': 2,
    '>': 4,
}

def matches(line, match = None):
    seeking = []
    for i, char in enumerate(line):
        if char in PAIRS:
            seeking.append(PAIRS[char])
        elif len(seeking) > 0 and char == seeking[-1]:
            seeking.pop()
        else:
            return (False, line[i:], seeking)

    if len(seeking) == 0:
        return (True, '', seeking)

    return (None, '', seeking)

def error_score(chars):
    return ERROR_POINTS[chars[0]]

def incomplete_score(chars):
    score = 0
    for c in reversed(chars):
        score *= 5
        score += INCOMPLETE_POINTS[c]
    return score

def median(xs):
    return sorted(xs)[len(xs) // 2]

all_matches = list(map(matches, lines))
errors = [remaining for (matched, remaining, missing) in all_matches if matched == False]
incomplete = [missing for (matched, remaining, missing) in all_matches if matched == None]

total_error_points = sum(map(error_score, errors))
print(total_error_points)

total_incomplete_scores = list(map(incomplete_score, incomplete))
print(median(total_incomplete_scores))
