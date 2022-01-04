from sys import stdin
from itertools import permutations, product

lines = [line.strip() for line in stdin.readlines()]

MINIMUM_OVERLAP = 12
DIMENSIONS = 3

def parse_scan_report(lines):
    beacons = None
    beacon_scans = []

    for line in lines:
        if len(line) == 0:
            continue

        if line.startswith('---'):
            beacons = set()
            beacon_scans.append(beacons)
            continue

        if beacons is None:
            raise ValueError('Attempting to parse a scan before the first scanner entry')

        beacons.add(tuple(int(n) for n in line.split(',')))

    return beacon_scans

def all_translations(beacons):
    for beacon in beacons:
        yield beacon, set(tuple(n - m for n, m in zip(entry, beacon)) for entry in beacons)

def all_rotations(beacons):
    rotations = product(*([[1,-1]] * DIMENSIONS))
    for rotation in rotations:
        yield set(tuple(n * r for n, r in zip(beacon, rotation)) for beacon in beacons)

def all_facings(beacons):
    for indexes in permutations(range(DIMENSIONS)):
        yield set(tuple(beacon[i] for i in indexes) for beacon in beacons)

def all_orientations(beacons):
    for facing in all_facings(beacons):
        for rotated in all_rotations(facing):
            for translation, translated in all_translations(rotated):
                yield translation, translated

def find_sufficient_overlap(aligned_beacons, unaligned_beacons):
    aligned_translations = all_translations(aligned_beacons)
    unaligned_orientations = list(all_orientations(unaligned_beacons))
    combinations = product(aligned_translations, unaligned_orientations)

    for (aligned_translation, translated_aligned_beacons), (unaligned_translation, reoriented_beacons) in combinations:
        if len(translated_aligned_beacons & reoriented_beacons) >= MINIMUM_OVERLAP:
            return aligned_translation, translated_aligned_beacons, unaligned_translation, reoriented_beacons

def align_to(aligned_beacons, unaligned_beacons):
    match = find_sufficient_overlap(aligned_beacons, unaligned_beacons)

    if match is None:
        return None

    aligned_translation, _, unaligned_translation, reoriented_beacons = match
    scanner_position = tuple(a - u for a, u in zip(aligned_translation, unaligned_translation))
    aligned_beacons = set(tuple(a + e for a, e in zip(aligned_translation, beacon)) for beacon in reoriented_beacons)

    return {'scanner': scanner_position, 'beacons': aligned_beacons}

def find_alignment(unaligned_beacons, aligned_beacons):
    alignment = align_to(aligned_beacons, unaligned_beacons)
    if alignment is not None:
        return alignment
    return None

def pluck(key, dictionaries):
    return [d[key] for d in dictionaries]

def align_reports(unaligned_reports):
    if len(unaligned_reports) == 0:
        return []

    aligned_beacons, *unaligned_beacons= unaligned_reports
    aligned_reports = [{'scanner': (0, 0), 'beacons': aligned_beacons}]

    while len(unaligned_beacons) > 0:
        alignments = [find_alignment(beacons, aligned_beacons) for beacons in unaligned_beacons]

        newly_aligned = list(filter(bool, alignments))
        aligned_reports.extend(newly_aligned) # type: ignore

        beacons = pluck('beacons', newly_aligned)
        aligned_beacons = aligned_beacons | set.union(*beacons)

        unaligned_beacons = [beacons for i, beacons in enumerate(unaligned_beacons) if alignments[i] is None]

        if len(newly_aligned) == 0:
            raise ValueError('Could not find an alignment for all of the reports')

    return aligned_reports

def distance(a, b):
    return sum(n - m for n, m in zip(a, b))

reports = parse_scan_report(lines)

aligned_reports = align_reports(reports)
aligned_beacons = [report['beacons'] for report in aligned_reports]
aligned_scanners = [report['scanner'] for report in aligned_reports]

all_beacons = set.union(*aligned_beacons)
print(len(all_beacons))

max_distance = max(distance(s1, s2) for s1, s2 in product(aligned_scanners, aligned_scanners))
print(max_distance)
