from sys import stdin
from enum import Enum, auto
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import NamedTuple, Iterable
from multiprocessing import Pool
from time import time
from functools import reduce
from operator import mul

class Material(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()

Currency = Counter[Material]

class Blueprint(NamedTuple):
    identifier: int
    prices: dict[Material, Currency]
    maximums: Counter[Material]

    @staticmethod
    def parse(line: str) -> 'Blueprint':
        label, rest = line.split(': ')
        identifier = int(label.split(' ')[1])
        prices = rest.split('. ')

        ore_robot_ore = int(prices[0].split(' ')[4])

        clay_robot_ore = int(prices[1].split(' ')[4])

        obsidian_robot_ore = int(prices[2].split(' ')[4])
        obsidian_robot_clay = int(prices[2].split(' ')[7])

        geode_robot_ore = int(prices[3].split(' ')[4])
        geode_robot_obsidian = int(prices[3].split(' ')[7])

        prices = {
            Material.ORE: Counter({Material.ORE: ore_robot_ore}),
            Material.CLAY: Counter({Material.ORE: clay_robot_ore}),
            Material.OBSIDIAN: Counter({Material.ORE: obsidian_robot_ore, Material.CLAY: obsidian_robot_clay}),
            Material.GEODE: Counter({Material.ORE: geode_robot_ore, Material.OBSIDIAN: geode_robot_obsidian}),
        }

        maximums = defaultdict(int)
        for _, price in prices.items():
            for material, amount in price.items():
                maximums[material] = max(amount, maximums[material])

        return Blueprint(identifier, prices, Counter(maximums))

@dataclass
class RobotFactory:
    blueprint: Blueprint
    robots: Counter[Material] = field(default_factory=lambda: Counter([Material.ORE]))
    resources: Counter[Material] = field(default_factory=Counter)

    def can_afford(self: 'RobotFactory', material: Material) -> bool:
        return self.blueprint.prices[material] <= self.resources

    def build_robot(self: 'RobotFactory', material: Material) -> 'RobotFactory':
        robots = self.robots.copy()
        resources = self.resources.copy()

        robots[material] += 1
        resources -= self.blueprint.prices[material]

        return RobotFactory(self.blueprint, robots, resources)

    def should_build(self: 'RobotFactory', material: Material, time: int, target: Material) -> bool:
        # Don't build anything we can't afford
        if not self.can_afford(material):
            return False

        # Always build more robots for our target resource (Geode, in this case)
        if material == target:
            return True

        # If we have enough robots to mine sufficient resources every round
        # to build anything using that resource, don't build any more
        if self.robots[material] >= self.blueprint.maximums[material]:
            return False

        # If we have enough resources and mining capacity that we could not
        # spend all of the resource no matter what we build, don't build any more
        expected_quantity = self.resources[material] + self.robots[material] * (time - 1)
        maximum_needed = self.blueprint.maximums[material] * time
        if expected_quantity >= maximum_needed:
            return False

        return True

    def build_robots(self: 'RobotFactory', time: int, target: Material, best_so_far: int) -> Iterable['RobotFactory']:
        absolute_maximum = self.resources[target] + (self.robots[target] * time) + (time * (time - 1) // 2)
        if absolute_maximum <= best_so_far:
            # Nothing we can build will beat our best, so build nothing
            return

        yield self # no-op build
        for material in Material:
            if self.should_build(material, time, target):
                yield self.build_robot(material)

    def cache_key(self: 'RobotFactory', time: int, target: Material) -> str:
        max_resources = self.blueprint.maximums

        # These keys use the same short-circuiting logic found in `should_build`.
        # e.g.
        #   cache key: min(self.robots[m], max_resources[m])
        #       versus
        #   should build: self.robots[m] >= self.blueprint.maximums[m]
        #
        #   and
        #
        #    cache key: min(self.resources[m] + (self.robots[m] * (time - 1)), max_resources[m] * time)
        #       versus
        #    should build: expected_quantity >= maximum_needed
        robots_key = [min(self.robots[m], max_resources[m]) if m != target else self.robots[m] for m in Material]
        resources_key = [min(self.resources[m] + (self.robots[m] * (time - 1)), max_resources[m] * time) if m != target else self.resources[m] for m in Material]

        return f"{time} {target} {robots_key} {resources_key}"

    def maximize_production(self: 'RobotFactory', time: int, target: Material = Material.GEODE) -> int:
        return self._maximize_production(time, target, {}, 0)

    def _maximize_production(self: 'RobotFactory', time: int, target: Material, cache: dict[str, int], maximum: int) -> int:
        if time == 0:
            return self.resources[target]

        cache_key = self.cache_key(time, target)
        if cache_key in cache:
            return cache[cache_key]

        # Store the robots we have prior to building new ones
        robots = self.robots.copy()

        # Build every combination of robots, including no-op, that we can with the current resources
        factories = list(self.build_robots(time, target, maximum))

        for factory in factories:
            # Collect the resources that we could have collected *prior* to building new robots
            factory.resources += robots

            # Move to the next time step for each factory
            maximum = max(maximum, factory._maximize_production(time - 1, target, cache, maximum))

        cache[cache_key] = maximum
        return maximum

blueprints = list(map(Blueprint.parse, stdin.read().splitlines()))
factories = list(map(RobotFactory, blueprints))

# Python multiprocessing requires the function that is passed to `pool.map`
# to be picklable, which means we need these two explicit functions instead
# lambdas or something else.
def part1(factory: RobotFactory) -> int:
    production = factory.maximize_production(24)
    return factory.blueprint.identifier * production

def part2(factory: RobotFactory) -> int:
    return factory.maximize_production(32)

with Pool(32) as p:
    # Part 1
    now = time()

    qualities = p.map(part1, factories)
    print(sum(qualities))
    print(time() - now)

    # Part 2
    now = time()

    geodes = p.map(part2, factories[:3])
    product = reduce(mul, geodes, 1)
    print(product)
    print(time() - now)
