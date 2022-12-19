from sys import stdin
from typing import NamedTuple, Iterator, Optional

class Point(NamedTuple):
    x: int
    y: int

class Interval(NamedTuple):
    lower: int
    upper: int

    def __str__(self):
        return f'({self.lower}, {self.upper})'

    def union(self: 'Interval', other: 'Interval') -> list['Interval']:
        if not self.touches(other):
            return sorted([self, other])

        new_lower = min(self.lower, other.lower)
        new_upper = max(self.upper, other.upper)
        return [Interval(new_lower, new_upper)]

    def touches(self: 'Interval', other: 'Interval') -> bool:
        adjacent = (self.upper + 1) == other.lower or (other.upper + 1) == self.lower
        overlaps = (self.lower <= other.upper and self.upper >= other.lower)
        return adjacent or overlaps

    def area(self: 'Interval') -> int:
        return max(0, self.upper - self.lower + 1)

    def clamp(self: 'Interval', bounds: 'Interval') -> 'Interval':
        lower = max(self.lower, bounds.lower)
        upper = min(self.upper, bounds.upper)
        return Interval(lower, upper)

    @staticmethod
    def union_all(intervals: list[Optional['Interval']]) -> list['Interval']:
        non_empty = [interval for interval in intervals if interval is not None]
        unioned = []
        for interval in sorted(non_empty):
            if len(unioned) == 0:
                unioned.append(interval)
                continue
            last = unioned.pop()
            unioned.extend(interval.union(last))
        return unioned

def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

class Sensor(NamedTuple):
    location: Point
    beacon: Point
    radius: int

    @staticmethod
    def new(location: Point, beacon: Point) -> 'Sensor':
        radius = manhattan_distance(location, beacon)
        return Sensor(location, beacon, radius)

    def coverage_at(self: 'Sensor', row: int) -> Optional[Interval]:
        vertical_distance = abs(self.location.y - row)
        if vertical_distance > self.radius:
            return None

        half_width = abs(vertical_distance - self.radius)
        start = self.location.x - half_width
        end = self.location.x + half_width

        return Interval(start, end)

def unioned_intervals(row: int, sensors: list[Sensor], bounds: Optional[Interval] = None) -> list[Interval]:
    coverage: list[Optional[Interval]] = [sensor.coverage_at(row) for sensor in sensors]

    if bounds is not None:
        coverage = [interval.clamp(bounds) for interval in coverage if interval is not None]

    return Interval.union_all(coverage)

def claimed_area(row: int, sensors: list[Sensor]) -> int:
    intervals = unioned_intervals(row, sensors)
    unioned_area = sum(interval.area() for interval in intervals)
    overlapping_sensors = set(sensor for sensor in sensors if sensor.location.y == row)
    overlapping_beacons = set(sensor.beacon for sensor in sensors if sensor.beacon.y == row)

    return unioned_area - len(overlapping_sensors) - len(overlapping_beacons)

def tuning_frequecy(row: int, intervals: list[Interval], bounds: Interval) -> int:
    col, multiplier = None, 4000000

    if len(intervals) == 2:
        col = intervals[0].upper + 1
    elif intervals[0].lower > bounds.lower:
        col = bounds.lower
    elif intervals[0].upper < bounds.upper:
        col = bounds.upper

    if col is None:
        raise Exception("Don't know how to compute this frequency.")

    return row + (col * multiplier)

def parse_xy(line: str) -> Point:
    tokens = line.split()
    x_token, y_token = tokens[-2:]

    x = int(x_token[2:-1])
    y = int(y_token[2:])
    return Point(x, y)

def parse_line(line: str) -> Sensor:
    sensor_portion, beacon_portion = line.split(': ')

    sensor = parse_xy(sensor_portion)
    beacon = parse_xy(beacon_portion)

    return Sensor.new(sensor, beacon)

sensors = list(map(parse_line, stdin.read().splitlines()))

# Part 1
print(claimed_area(2000000, sensors))

# Part 2
bounds = Interval(0, 4000000)
for row in range(0, 4000000):
    unioned = unioned_intervals(row, sensors, bounds)
    area = sum(interval.area() for interval in unioned)
    if area < bounds.area():
        print(tuning_frequecy(row, unioned, bounds))
        break
