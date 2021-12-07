from sys import stdin

lines = [line.strip().split(',') for line in stdin.readlines()]
positions = [int(age) for age in lines[0]]

min_pos = min(positions)
max_pos = max(positions)

def fuel_for_distance(distance):
    distance = abs(distance)
    return (distance * (distance + 1)) / 2

def required_fuel(pos, positions):
    return sum(fuel_for_distance(pos - p) for p in positions)

fuel_at_positions = ((required_fuel(pos, positions), pos) for pos in range(min_pos, max_pos + 1))
(cheapest_fuel, cheapest_position) = min(fuel_at_positions)
print(cheapest_fuel)
