import re

cards = {}

def parse(input: list[str]):
    for line in input:
        line = line.strip()
        if len(line) == 0: continue
        (cardname, stuff) = line.split(":")
        (winningnumbers, numbers) = stuff.split("|")

        m = re.search('\d+', cardname)
        cardnum = int(m.group(0))


        numbers = set([int(x.strip()) for x in numbers.split(" ") if len(x) > 0])
        winningnumbers = set([int(x.strip()) for x in winningnumbers.split(" ") if len(x) > 0])
        
        matches = numbers.intersection(winningnumbers)

        #print(cardname, numbers, winningnumbers, matches, points)
        cards[cardnum] = len(matches)

    print(f"Parsed {len(cards)} cards")

def part1(input: list[str]):
    parse(input)
    return sum([2**(matches-1) for matches in cards.values() if matches>0 ])

def part2(input: list[str]):
    if len(cards) == 0:
        parse(input)

    cardlist = list(cards.keys())
    cardlist.sort()
    cardcount = {x:1 for x in cardlist}

    for c in cardlist:
        p = cards[c]
        n = cardcount[c]
        newcards = cardlist[c:c+p]
        #print(f"{n} copies of card {c} with {p} points")
        #print(newcards)
        for x in newcards:
            cardcount[x] += n
        #print(cardcount)
        #print()

    totalcards = sum(cardcount.values())
    return totalcards