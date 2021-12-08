from sys import stdin
from itertools import permutations

lines = [line.strip().split(' | ') for line in stdin.readlines()]
readings = [(observation.split(' '), obfuscated_digits.split(' ')) for observation, obfuscated_digits in lines]

digits_to_segments = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg',
]

connections = 'abcdefg'
connection_permutations = [''.join(permutation) for permutation in permutations(connections)]
translations = [str.maketrans(permutation, connections) for permutation in connection_permutations]

def translate(observation, translation):
    return ''.join(sorted(observation.translate(translation)))

def is_valid(observation, translation):
    return translate(observation, translation) in digits_to_segments

def observation_to_digit(observation, translation):
    translation = translate(observation, translation)
    return digits_to_segments.index(translation)

def find_translation(signal):
    for translation in translations:
        if all(is_valid(observation, translation) for observation in signal):
            return translation

def to_number(digits):
    number, shift = 0, 1
    for digit in reversed(digits):
        number += digit * shift
        shift *= 10
    return number

def reading_to_digits(reading):
    observation, obfuscated_digits = reading
    translation = find_translation(observation)

    if translation is None:
        raise Exception('No translation found')

    return [observation_to_digit(digit, translation) for digit in obfuscated_digits]

counts = 0
total = 0

for reading in readings:
    digits = reading_to_digits(reading)
    counts += sum(1 for digit in digits if digit in [1,4,7,8])
    total += to_number(digits)

print(counts)
print(total)
