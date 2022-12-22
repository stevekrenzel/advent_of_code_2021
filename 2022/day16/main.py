from sys import stdin
from typing import NamedTuple

class Valve(NamedTuple):
    name: str
    rate: int
    neighbors: list['Valve']

# The only state we care about for an actor is what valve they are at... so actors are just synonyms for valves
Actor = Valve

def max_pressure(actors: list[Actor], time: int) -> int:
    # This is just a helper fn to initialize some the cache and whatnot for `recurse`
    # It makes the callsite a little cleaner
    return recurse(actors, time, time, [], {})

def recurse(actors: list[Actor], time: int, total_time: int, opened: list[str], cache: dict[str, int]) -> int:
    # If there are no actors remaining, we're done.
    if len(actors) == 0:
        return 0

    # We explore all the paths of whatever actor is at the head of the list
    valve = actors[0]

    # Check if we've already seen these positions at this time with this set of opened valves
    cache_key = f'{sorted([valve.name for valve in actors])} {time} {sorted(opened)}'
    if cache_key in cache:
         return cache[cache_key]

    # We've hit a leaf node for this valve. This leaf now becomes the root
    # of the depth-first search for the next actor, where we start the search
    # from the start, but with a shared cache and set of opened valves
    if time <= 1:
        return recurse(actors[1:], total_time, total_time, opened, cache)

    # Try moving to each neighbor without opening my valve
    moving = max(recurse([neighbor] + actors[1:], time - 1, total_time, opened, cache) for neighbor in valve.neighbors)

    # If we haven't opened my valve and it has a rate, open it!
    should_open = valve.rate > 0 and valve.name not in opened
    pressure = valve.rate * (time - 1)
    opening = (pressure + recurse(actors, time - 1, total_time, opened + [valve.name], cache)) if should_open else 0

    most_pressure = max(moving, opening)
    cache[cache_key] = most_pressure
    return most_pressure

def parse_valve(line: str) -> Valve:
    name = line[6:8]
    rate = int(line.split('=')[-1])
    return Valve(name , rate, [])

def parse_tunnels(line: str) -> list[str]:
    divider = 'valves ' if 'tunnels' in line else 'valve '
    tunnels = line.split(divider)[-1]
    return tunnels.split(', ')

def parse_lines(lines: list[str]) -> dict[str, Valve]:
    valves = {}
    mapping = {}

    for line in lines:
        valve_line, tunnels_line = line.split('; ')

        valve = parse_valve(valve_line)
        tunnels = parse_tunnels(tunnels_line)

        valves[valve.name] = valve
        mapping[valve.name] = tunnels

    for valve_name, tunnels in mapping.items():
        neighbors = [valves[tunnel] for tunnel in tunnels]
        neighbors.sort(key=lambda neighbor: neighbor.rate)
        valves[valve_name].neighbors.extend(neighbors)

    return valves

valves = parse_lines(stdin.read().splitlines())

# Part 1
print(max_pressure([valves['AA']], 30))

# Part 2
print(max_pressure([valves['AA'], valves['AA']], 26))
