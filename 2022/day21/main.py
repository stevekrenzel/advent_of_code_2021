from sys import stdin
from typing import Callable
from dataclasses import dataclass

@dataclass
class Expressions(dict):
    definitions: dict[str, str]
    helpers: dict[str, Callable]

    def __getitem__(self, key):
        return int(eval(self.definitions[key], self.helpers, self))

def search(expressions, key, value, lower, upper):
    while lower < upper:
        mid = (lower + upper) // 2
        expressions.definitions[key] = str(mid)
        val = expressions[value]

        if val < 0:
            upper = mid - 1
        elif val > 0:
            lower = mid + 1
        else:
            return mid

helpers = { "compare": lambda a, b: -1 if a < b else 1 if a > b else 0 }
mapping = dict(line.split(': ') for line in stdin.read().splitlines())
expressions = Expressions(mapping, helpers)

# Part 1
print(expressions['root'])

# Part 2
root = expressions.definitions['root']
a, b = root.split(' + ')
expressions.definitions['root'] = f'compare({a}, {b})'
print(search(expressions, 'humn', 'root', -2**64, 2**64))
