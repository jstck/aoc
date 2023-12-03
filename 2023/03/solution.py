import re


def checksymbol(x1, x2, y, input, n):

    ymax = len(input)
    xmax = len(input[0])

    left = max(x1-1, 0)
    right = min(x2+1, xmax-1)

    border = ""

    if y>0:
        border += input[y-1][left:right]

    if y<ymax-1:
        border += input[y+1][left:right]

    if x1 > 0:
        border += input[y][x1-1]

    if x2 < xmax:
        border += input[y][x2]

    m = re.search('[^0-9.]', border)
    f = (m != None)

    #print(f"Row {y} {n:3} {border}: {f}   x1:{x1} x2:{x2} left:{left} right:{right}")
    #print()

    return f

def part1(input: list[str]):
    sum = 0

    for y, line in enumerate(input):
        matches = re.findall('[0-9]+', line)

        startpos = 0
        for n in matches:
            x1 = line.find(n, startpos)
            x2 = x1 + len(n)

            #print(n, x1,x2,y)

            startpos = x2 + 1

            if checksymbol(x1, x2, y, input, n):
                #print(n)
                sum += int(n)


    return sum

#def part2(input: list[str]):
#    return ""
