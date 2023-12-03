import re
import sys

digits = set([str(x) for x in range(0,10)])


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

    print(f"Row {y} {n:3} {border}: {f}   x1:{x1} x2:{x2} left:{left} right:{right}")
    print()

    return f

def yoinkleft(s: str) -> str:
    m = re.search('^[0-9]+', s)
    if m is None:
        return ""
    return m.group(0)

def yoinkright(s: str) -> str:
    return yoinkleft(s[::-1])[::-1]

def yoinkfrom(s: str, x: int)-> list[str]:
    leftbit = yoinkright(s[:x])
    mid = s[x]
    rightbit = yoinkleft(s[x+1:])

    if mid in digits:
        return [leftbit+mid+rightbit]
    else:
        return [x for x in [leftbit, rightbit] if len(x)>0]

def checkgear(x,y,input):
    #Double check we're in the right spot
    if input[y][x] != "*":
        print(f"WARNING!! row {y} col {x} not *", file=sys.stderr)

    ymax = len(input)
    xmax = len(input[0])

    nums = []

    #Check straight left
    if x>0:
        c = input[y][x-1]
        if c in digits:
            #print("Stuff to left")
            nums.append(yoinkright(input[y][:x]))

    #Check straight right
    if x<xmax-1:
        c = input[y][x+1]
        if c in digits:
            #print("Stuff to right")
            nums.append(yoinkleft(input[y][x+1:]))

    #Check up:
    if y>0:
        line = input[y-1]
        nums += yoinkfrom(line, x)

    #Check down:
    if y<ymax-1:
        line = input[y+1]
        nums += yoinkfrom(line, x)

    nums = [int(x) for x in nums]
    if len(nums) == 2:
        return nums[0]*nums[1]
    
    return 0

def part2(input: list[str]):
    sum = 0
    grid = [list(x) for x in input]

    for y, line in enumerate(input):
        matches = re.findall('\*', line)

        startpos = 0
        for n in matches:
            x1 = line.find(n, startpos)
            x2 = x1 + len(n)

            #print(f"{n} row {y:3} col {x1:3}")

            ratio = checkgear(x1, y, input)

            if ratio>0:
                sum += ratio

            startpos = x2

            

    return sum
