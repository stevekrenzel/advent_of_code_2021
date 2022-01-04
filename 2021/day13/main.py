from sys import stdin
from collections import defaultdict, Counter

lines = [line.strip() for line in stdin.readlines()]

def parse(lines):
    dots = set()
    folds = []
    for line in lines:
        if ',' in line:
            (x, y) = map(int, line.split(','))
            dots.add((x, y))

        elif 'fold along y' in line:
            (_, y) = line.split('=')
            folds.append(('horizontal', int(y)))

        elif 'fold along x' in line:
            (_, x) = line.split('=')
            folds.append(('vertical', int(x)))

    return (dots, folds)

def horizontal_fold(fold_point, dots):
    folded_dots = set()

    for (x, y) in dots:
        folded_dots.add((x, fold_point - abs(y - fold_point)))

    return folded_dots

def vertical_fold(fold_point, dots):
    folded_dots = set()

    for (x, y) in dots:
        folded_dots.add((fold_point - abs(x - fold_point), y))

    return folded_dots

def dots_string(dots):
    min_x = min(x for (x, _) in dots)
    max_x = max(x for (x, _) in dots)
    min_y = min(y for (_, y) in dots)
    max_y = max(y for (_, y) in dots)

    lines = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            char = '█' if (x, y) in dots else ' '
            row.append(char)
        lines.append(''.join(row))

    return '\n'.join(lines)

def process_folds(folds, dots):
    for (orientation, fold_point) in folds:
        if orientation == 'horizontal':
            dots = horizontal_fold(fold_point, dots)
        elif orientation == 'vertical':
            dots = vertical_fold(fold_point, dots)
    return dots

(dots, folds) = parse(lines)

one_fold = process_folds(folds[:1], dots)
print(len(one_fold))

dots = process_folds(folds, dots)
print(dots_string(dots))
