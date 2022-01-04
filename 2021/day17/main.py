from sys import stdin
import re

lines = [line.strip() for line in stdin.readlines()]

def parse_target_area(line):
    regex = r'x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)'
    match = re.search(regex, line)

    if match is None:
        return None

    x1 = int(match.group('x1'))
    x2 = int(match.group('x2'))
    y1 = int(match.group('y1'))
    y2 = int(match.group('y2'))

    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = max(y1, y2), min(y1, y2)

    return {'x-range': (x1, x2), 'y-range': (y1, y2)}

def intersects(point, target_area):
    x, y = point
    x1, x2 = target_area['x-range']
    y1, y2 = target_area['y-range']

    return x1 <= x <= x2 and y1 >= y >= y2

def move(point, velocity):
    x, y = point
    dx, dy = velocity

    return (x + dx, y + dy)

def drag(velocity):
    x, y = velocity

    if x == 0:
        return (x, y)

    if x > 0:
        return (x - 1, y)

    return (x + 1, y)

def gravity(velocity):
    x, y = velocity

    return (x, y - 1)

def step(point, velocity):
    new_point = move(point, velocity)
    new_velocity = gravity(drag(velocity))
    return new_point, new_velocity

def simulate(velocity):
    point = (0, 0)
    while True:
        point, velocity = step(point, velocity)
        yield point, velocity

def is_impossible(point, velocity, target_area):
    x, y = point
    dx, dy = velocity

    x1, x2 = target_area['x-range']
    _, y2 = target_area['y-range']

    if dx == 0 and (x < x1 or x > x2):
        return True

    if dx > 0 and x > x2:
        return True

    if dx < 0 and x < x1:
        return True

    if dy < 0 and y < y2:
        return True

    return False


def hits_target(velocity, target_area):
    highest_point = (0, 0)

    for p, v in simulate(velocity):
        if highest_point is None or p[1] > highest_point[1]:
            highest_point = p

        if intersects(p, target_area):
            return True, highest_point

        if is_impossible(p, v, target_area):
            return False, highest_point

    return False, highest_point

def grid_search(target_area):
    test_velocities = ((dx, dy) for dx in range(-200, 200) for dy in range(-200, 200))
    for velocity in test_velocities:
        hits, highest_point = hits_target(velocity, target_area)
        if hits:
            yield velocity, highest_point

def find_max_altitude_velocity(target_area):
    hit_velocities = grid_search(target_area)
    return max(hit_velocities, key=lambda v: v[1][1])

for line in lines:
    target_area = parse_target_area(line)
    print(find_max_altitude_velocity(target_area)[1][1])
    print(len(set(grid_search(target_area))))
