import sys

part1 = 0
part2 = 0

def maxjolt(batteries: list[int], n: int) -> list[int]:
    if n==1:
        return [max(batteries)]
    
    #Pick the biggest number saving the remaining n-1 ones
    remainder = n-1
    firstbat = max(batteries[:-remainder])

    #Find position of that first battery
    firstpos = batteries.index(firstbat)

    #Do the rest recursively
    return [firstbat] + maxjolt(batteries[firstpos+1:], remainder)


for l in sys.stdin.readlines():
    b = [int(c) for c in list(l.strip())]

    best = 0

    for x in range(0, len(b)-1):
        for y in range(x+1, len(b)):
            jolt = b[x]*10+b[y]
            best = max(best, jolt)


    p1 = int("".join([str(x) for x in maxjolt(b, 2)]))
    p2 = int("".join([str(x) for x in maxjolt(b, 12)]))

    part1 += p1
    part2 += p2

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")