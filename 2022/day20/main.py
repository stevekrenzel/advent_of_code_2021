from sys import stdin

def shift(x, xs):
    old_index = xs.index(x)
    del xs[old_index]

    new_index = (old_index + x[1]) % len(xs)
    xs.insert(new_index, x)

def decrypt(numbers, rounds=1):
    indexed = list(enumerate(numbers))
    for _ in range(rounds):
        for current in enumerate(numbers):
            shift(current, indexed)
    return [n for _, n in indexed]

def key(numbers, indexes=[1000, 2000, 3000]):
    zero_index = next(i for i, n in enumerate(numbers) if n == 0)
    return sum(numbers[(zero_index + i) % len(numbers)] for i in indexes)

numbers = list(map(int, stdin.read().splitlines()))

# Part 1
print(key(decrypt(numbers)))

# Part 2
multiplied = [n * 811589153 for n in numbers]
print(key(decrypt(multiplied, 10)))
