from sys import stdin
from itertools import zip_longest
from heapq import heappush, heappop
from collections import defaultdict

ENERGEY_PER_MOVE = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def parse_world(lines):
    width = range(len(lines[0]))
    world = [[c for _, c in zip_longest(width, line, fillvalue=' ')] for line in lines]

    labeled_world = []
    rooms = defaultdict(list)
    positions = {}
    for y, row in enumerate(world):
        room_order = ['A', 'B', 'C', 'D']
        labeled_row = []
        for x, c in enumerate(row):
            if c in '#. ':
                labeled_row.append(c)
            else:
                room = room_order.pop(0)
                labeled_row.append(room)
                rooms[room].append((x, y))
                positions[(x, y)] = c
        labeled_world.append(labeled_row)
    return positions, rooms, labeled_world

def is_wall(position, world):
    x, y = position
    return world[y][x] == '#'

def is_occupied(position, positions):
    return position in positions

def is_room(position, world):
    x, y = position
    return world[y][x] in 'ABCD'

def is_hallway(position, world):
    x, y = position
    return world[y][x] == '.'

def room_assignment(position, world):
    x, y = position
    return world[y][x]

def is_blocking_room(position, world):
    x, y = position
    return is_hallway(position, world) and is_room((x, y + 1), world)

def is_room_packed_tight(species, positions, rooms):
    room = rooms[species]

    validating = False
    for spot in sorted(room):
        if is_occupied(spot, positions):
            validating = True

        if not validating:
            continue

        if not is_occupied(spot, positions):
            return False

        if positions[spot] != species:
            return False

    return True

def is_traversable(destination, positions, world):
    return not (is_wall(destination, world) or is_occupied(destination, positions))

def neighbors(position, positions, world):
    x, y = position
    width, height = len(world[0]), len(world)

    if x > 0 and is_traversable((x-1, y), positions, world):
        yield (x - 1, y)

    if x < width - 1 and is_traversable((x+1, y), positions, world):
        yield (x + 1, y)

    if y > 0 and is_traversable((x, y-1), positions, world):
        yield (x, y - 1)

    if y < height - 1 and is_traversable((x, y+1), positions, world):
        yield (x, y + 1)

def reachable_from(position, positions, world, cost=0, species=None, visited=None):
    if visited is None:
        visited = set()

    if species is None:
        species = positions[position]

    if position in visited:
        return
    visited.add(position)

    energy = ENERGEY_PER_MOVE[species]
    new_cost = cost + energy

    for neighbor in neighbors(position, positions, world):
        if neighbor in visited:
            continue
        yield new_cost, neighbor
        yield from reachable_from(neighbor, positions, world, new_cost, species, visited)

def can_stop_here(old_position, new_position, positions, rooms, world):
    species = positions[old_position]
    if is_blocking_room(new_position, world):
        return False

    ended_in_room = is_room(new_position, world)
    if ended_in_room:
        if room_assignment(new_position, world) != species:
            return False

        if not is_room_packed_tight(species, positions, rooms):
            return False

        return True

    started_in_hallway = is_hallway(old_position, world)
    ended_in_hallway = is_hallway(new_position, world)
    if started_in_hallway and ended_in_hallway:
        return False

    return True

def move_from(old_position, new_position, positions):
    if old_position == new_position:
        return positions

    new_positions = positions.copy()
    new_positions[new_position] = positions[old_position]
    del new_positions[old_position]
    return new_positions

def is_complete(positions, world):
    in_correct_room = lambda position: room_assignment(position, world) == positions[position]
    return all(in_correct_room(position) for position in positions)

def next_positions(positions, rooms, world):
    for old_position, species in positions.items():
        is_tight = is_room_packed_tight(species, positions, rooms)
        if room_assignment(old_position, world) == species and is_tight:
            continue
        for cost, new_position in reachable_from(old_position, positions, world):
            if can_stop_here(old_position, new_position, positions, rooms, world):
                new_positions = move_from(old_position, new_position, positions)
                if is_tight and not is_room_packed_tight(species, new_positions, rooms):
                    continue
                yield cost, new_positions, (old_position, new_position)

def minimum_energy_for_position(initial_position, positions):
    species = positions[initial_position]
    energy = ENERGEY_PER_MOVE[species]
    room_offsets = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
    return abs(room_offsets[species] - initial_position[0]) * energy

def minimum_energy_for_positions(positions):
    return sum(minimum_energy_for_position(position, positions) for position in positions.keys())

def search(positions, rooms, world):
    count = 0
    queue = [(0, 0, 0, positions)]
    visited = set()
    while len(queue) > 0:
        _, cost, _, positions = heappop(queue)

        if is_complete(positions, world):
            return cost, positions

        for additional_cost, next_position, _ in next_positions(positions, rooms, world):
            items = tuple(sorted(next_position.items()))
            if items in visited:
                continue
            visited.add(items)

            count += 1
            new_cost = cost + additional_cost
            heuristic = new_cost + minimum_energy_for_positions(next_position)

            heappush(queue, (heuristic, new_cost, count, next_position))
    return (None, None, None)

def print_world(positions, world):
    for y, row in enumerate(world):
        layout = ''.join(c.lower() for c in row)
        amphipods = ''.join(positions[(x,y)] if (x, y) in positions else ('.' if c in 'ABCD' else c) for x, c in enumerate(row))
        print(layout + ' ' + amphipods)

# Part 1
lines = stdin.read().splitlines()
positions, rooms, world = parse_world(lines)
cost, _ = search(positions, rooms, world)
print(cost)

# Part 2
lines = lines[:3] + ['  #D#C#B#A#  ', '  #D#B#A#C#  '] + lines[3:]
positions, rooms, world = parse_world(lines)
cost, _ = search(positions, rooms, world)
print(cost)
