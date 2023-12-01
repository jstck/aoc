import solution

def part2(input: list[str]):
    d = {
        "zero": "z0o",
        "one": "o1e",
        "two": "t2o",
        "three": "t3e",
        "four": "f4r",
        "five": "f5e",
        "six": "s6x",
        "seven": "s7n",
        "eight": "e8t",
        "nine": "n9e",
    }

    sum = 0
    for line in input:
        line = line.strip()

        for (word, digit) in d.items():
            line = line.replace(word, digit)

        digits = [int(x) for x in list(line) if x in "0123456789"]
        first = digits[0]
        last = digits[-1]
        cal = first*10+last
        sum += cal

    return sum
