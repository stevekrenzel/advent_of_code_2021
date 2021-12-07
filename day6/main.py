from sys import stdin

lines = [line.strip().split(',') for line in stdin.readlines()]
ages = [int(age) for age in lines[0]]

def summarize(ages):
    counts = [0] * 9
    for age in ages:
        counts[age] += 1
    return counts

def simulate(days, ages):
    summary = summarize(ages)
    for _ in range(days):
        breeding_fish = summary[0]
        summary = summary[1:] + [0]
        summary[6] += breeding_fish
        summary[8] += breeding_fish
    return summary

print(sum(simulate(80, ages)))
print(sum(simulate(256, ages)))
