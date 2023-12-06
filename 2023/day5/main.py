from sys import stdin
from re import split
from typing import NamedTuple

class Range(NamedTuple):
    start: int
    end: int

    def map_to(self, key, destination):
        if (key.start >= self.end) or (key.end <= self.start):
            return None, []

        remainder = []
        if key.start < self.start:
            remainder.append(Range(key.start, self.start))

        if key.end > self.end:
            remainder.append(Range(self.end, key.end))

        overlap = Range(max(key.start, self.start), min(key.end, self.end))

        new_start = destination.start + (overlap.start - self.start)
        new_end = destination.start + (overlap.end - self.start)
        return Range(new_start, new_end), remainder

    @staticmethod
    def parse_singletons(raw: str):
        starts = map(int, raw.strip().split(' '))
        return [Range(start, start + 1) for start in starts]

    @staticmethod
    def parse_ranges(raw: str):
        numbers = [int(r) for r in raw.strip().split(' ')]
        starts, sizes = numbers[::2], numbers[1::2]
        return [Range(start, start + size) for start, size in zip(starts, sizes)]

class SourceToDestinationRange(NamedTuple):
    source: Range
    destination: Range

    def map_to(self, other: Range):
        return self.source.map_to(other, self.destination)

    @staticmethod
    def parse(raw: str):
        destination_start, source_start, size = map(int, raw.split(' '))
        source = Range(source_start, source_start + size)
        destination = Range(destination_start, destination_start + size)
        return SourceToDestinationRange(source, destination)

class SourceToDestinationMap(NamedTuple):
    ranges: [SourceToDestinationRange]

    def destination(self, sources):
        sources, destinations = sources[:], []
        for source in sources:
            for range in self.ranges:
                destination, remainder = range.map_to(source)
                if destination is not None:
                    destinations.append(destination)
                    sources.extend(remainder)
                    break
            else:
                destinations.append(source)
        return sorted(destinations)

    @staticmethod
    def parse(raw: str):
        lines = raw.strip().split('\n')
        _label, *lines = lines
        ranges = [SourceToDestinationRange.parse(line) for line in lines]
        return SourceToDestinationMap(ranges)

class Almanac(NamedTuple):
    seed_to_soil: SourceToDestinationMap
    soil_to_fertilizer: SourceToDestinationMap
    fertilizer_to_water: SourceToDestinationMap
    water_to_light: SourceToDestinationMap
    light_to_temperature: SourceToDestinationMap
    temperature_to_humidity: SourceToDestinationMap
    humidity_to_location: SourceToDestinationMap

    def seed_to_location(self, seed):
        soil = self.seed_to_soil.destination(seed)
        fertilizer = self.soil_to_fertilizer.destination(soil)
        water = self.fertilizer_to_water.destination(fertilizer)
        light = self.water_to_light.destination(water)
        temperature = self.light_to_temperature.destination(light)
        humidity = self.temperature_to_humidity.destination(temperature)
        location = self.humidity_to_location.destination(humidity)
        return location

    def locations(self, seeds):
        return {seed: self.seed_to_location([seed]) for seed in seeds}

    @staticmethod
    def parse(groups: [str]):
        seed_to_soil = SourceToDestinationMap.parse(groups[0])
        soil_to_fertilizer = SourceToDestinationMap.parse(groups[1])
        fertilizer_to_water = SourceToDestinationMap.parse(groups[2])
        water_to_light = SourceToDestinationMap.parse(groups[3])
        light_to_temperature = SourceToDestinationMap.parse(groups[4])
        temperature_to_humidity = SourceToDestinationMap.parse(groups[5])
        humidity_to_location = SourceToDestinationMap.parse(groups[6])

        return Almanac(seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location)

raw = stdin.read()
groups = raw.split('\n\n')

raw_seeds = groups[0].split(': ')[1]
singletons = Range.parse_singletons(raw_seeds)
ranges = Range.parse_ranges(raw_seeds)

almanac = Almanac.parse(groups[1:])

# Part 1
print(min(almanac.locations(singletons).values())[0].start)

# Part 2
print(min(almanac.locations(ranges).values())[0].start)
