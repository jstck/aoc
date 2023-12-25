def part1(input: list[str]):
    sum = 0
    for line in input:
        digits = [int(x) for x in list(line.strip()) if x in "0123456789"]
        first = digits[0]
        last = digits[-1]
        cal = first*10+last
        sum += cal

    return sum

#def part2(input: list[str]):
#    return ""
