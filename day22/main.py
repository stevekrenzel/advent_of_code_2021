from sys import stdin
from re import search
from bisect import bisect_left, bisect_right
from itertools import product

def line_to_range(line):
    line_pattern = r'(?P<command>on|off) x=(?P<x1>-?\d+)..(?P<x2>-?\d+),y=(?P<y1>-?\d+)..(?P<y2>-?\d+),z=(?P<z1>-?\d+)..(?P<z2>-?\d+)'
    match = search(line_pattern, line)

    if match is None:
        raise ValueError('Invalid line: {}'.format(line))

    command = match.group('command')
    x1 = int(match.group('x1'))
    x2 = int(match.group('x2')) + 1
    y1 = int(match.group('y1'))
    y2 = int(match.group('y2')) + 1
    z1 = int(match.group('z1'))
    z2 = int(match.group('z2')) + 1

    return (command, ((x1, x2), (y1, y2), (z1, z2)))

def all_coordinates(cuboids):
    all_xs = sorted(set(x for (xs, _, _) in cuboids for x in xs))
    all_ys = sorted(set(y for (_, ys, _) in cuboids for y in ys))
    all_zs = sorted(set(z for (_, _, zs) in cuboids for z in zs))
    return (all_xs, all_ys, all_zs)

def slice(cube, all_coords):
    all_xs, all_ys, all_zs = all_coords
    (x1, x2), (y1, y2), (z1, z2) = cube

    unioned = set()
    xs = all_xs[bisect_left(all_xs, x1):bisect_right(all_xs, x2)]
    ys = all_ys[bisect_left(all_ys, y1):bisect_right(all_ys, y2)]
    zs = all_zs[bisect_left(all_zs, z1):bisect_right(all_zs, z2)]

    unioned.update(product(zip(xs, xs[1:]), zip(ys, ys[1:]), zip(zs, zs[1:])))
    return unioned

def volume(cube):
    (x1, x2), (y1, y2), (z1, z2) = cube
    return (x2 - x1) * (y2 - y1) * (z2 - z1)

def intersect(cube1, cube2):
    (x1, x2), (y1, y2), (z1, z2) = cube1
    (x3, x4), (y3, y4), (z3, z4) = cube2

    return ((max(x1, x3), min(x2, x4)), (max(y1, y3), min(y2, y4)), (max(z1, z3), min(z2, z4)))

def is_empty(cube):
    (x1, x2), (y1, y2), (z1, z2) = cube
    return x1 >= x2 or y1 >= y2 or z1 >= z2

def process_commands(commands, bound=None):
    command_regions = [cuboid for (_, cuboid) in commands]
    if bound is not None:
        command_regions = [intersect(bound, region) for region in command_regions]
        command_regions = [region for region in command_regions if is_empty(region) == False]

    all_cubes = set()
    all_coords = all_coordinates(command_regions)

    for command, cuboid in commands:
        cubes = slice(cuboid, all_coords)
        if command == 'on':
            all_cubes.update(cubes)
        elif command == 'off':
            all_cubes.difference_update(cubes)

    return sum(map(volume, all_cubes))

commands = [line_to_range(line.strip()) for line in stdin.readlines()]
intialization_area = ((-50, 50), (-50, 50), (-50, 50))
print(process_commands(commands, intialization_area))
print(process_commands(commands))
