def part1(input: list[str]):
    times = [int(x) for x in input[0].split(":")[1].split()]
    distances = [int(x) for x in input[1].split(":")[1].split()]

    winlist = []

    for (i, t) in enumerate(times):
        d = distances[i]
        print(t, d)
        wins = 0
        for chargetime in range(1, t):
            timeremaining = t - chargetime
            traveled = timeremaining * chargetime
            if traveled > d:
                wins += 1

        winlist.append(wins)

    print(winlist)



    return math.prod(winlist)

def part2(input: list[str]):
    times = [x for x in input[0].split(":")[1].split()]
    distances = [x for x in input[1].split(":")[1].split()]

    t = int("".join(times))
    d = int("".join(distances))

    print(t, d)
    wins = 0
    for chargetime in range(1, t):
        timeremaining = t - chargetime
        traveled = timeremaining * chargetime
        if traveled > d:
            wins += 1

    print(wins)
    return wins
