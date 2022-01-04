from sys import stdin

commands = [line.strip().split() for line in stdin.readlines()]
for command in commands:
    if len(command) == 2:
        command.append('')

# Key values, from provided input, for reference
# X = [ 13, 11, 15, -6, 15, -8, -4, 15, 10, 11, -11,  0, -8, -7]
# Y = [  3, 12,  9, 12,  2,  1,  1, 13,  1,  6,   2, 11, 10,  3]
# Z = [  1,  1,  1, 26,  1, 26, 26,  1,  1,  1,  26, 26, 26, 26]

def commands_to_key_values(commands):
    xs, ys, zs = [], [], []
    for i, (_, _, value) in enumerate(commands):
        if i % 18 == 4:
            zs.append(int(value))
        if i % 18 == 5:
            xs.append(int(value))
        if i % 18 == 15:
            ys.append(int(value))
    return xs, ys, zs

def find_all(xs, ys, ws=[], stack=[0]):
    if len(xs) == 0:
        yield ws
        return

    x, *xs = xs
    y, *ys = ys
    head, *tail = stack

    for w in range(1, 10):
        if x > 0 and x + head != w:
            yield from find_all(xs, ys, ws + [w], [w + y] + stack)
        elif x <= 0 and x + head == w:
            yield from find_all(xs, ys, ws + [w], tail)

xs, ys, _ = commands_to_key_values(commands)

print(max(find_all(xs, ys)))
print(min(find_all(xs, ys)))
