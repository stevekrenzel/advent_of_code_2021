from sys import stdin
import re

lines = stdin.readlines()

NON_DIGIT_CHARS = r"[^0-9]"

WORD_TO_NUMBER = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def remove_non_digits(line):
    return re.sub(NON_DIGIT_CHARS, '', line)

def line_to_number(line):
    digits_only = remove_non_digits(line)
    return int(digits_only[0] + digits_only[-1])

def replace_words_with_numbers(line):
    output = []
    for i, c in enumerate(line):
        for number_word, number in WORD_TO_NUMBER.items():
            is_word = line[i:].startswith(number_word)
            output.append(number if is_word else c)
    return ''.join(output)

# Part 1
print(sum(map(line_to_number, lines)))

# Part 2
deworded = map(replace_words_with_numbers, lines)
print(sum(map(line_to_number, deworded)))
