#!/usr/bin/env python3

import sys
from collections import Counter
#  0000
# 1    2
# 1    2
#  3333
# 4    5
# 4    5
#  6666

result = 0

for line in sys.stdin.readlines():
    (input, output) = line.strip().split("|", 1)

    input = [set(list(s.strip())) for s in input.split() ]
    output = [set(list(s.strip())) for s in output.split() ]

    alldigits = input + output

    ones = [ d for d in alldigits if len(d)==2 ]
    fours = [ d for d in alldigits if len(d)==4 ]
    sevens = [ d for d in alldigits if len(d)==3 ]

    #Known digits
    one = ones[0]
    four = fours[0]
    seven = sevens[0]
    eight = set(list("abcdefg"))

    #Top segment is in 7 but not 1
    seg0 = list(seven - one)[0]

    #Right-side segments are in 1
    seg25 = one

    #Stuff in 4 but not 1
    seg13 = four - one


    #Zeroes, sixes and nines all have 6 elements
    zerosixnine = [ d for d in alldigits if len(d)==6 ]

    #Six is the group that has exactly one out of segments 2 and 5 (seg5)
    for s in zerosixnine:
        if len(s & seg25) == 1:
            seg5 = list(s & seg25)[0]
            six = s
            break

    #Six is just missing seg2
    seg2 = list(eight - six)[0]

    #zero is the group that has exactly one out of segments 1 and 3 (seg1)
    for s in zerosixnine:
        if len(s & seg13) == 1:
            seg1 = list(s & seg13)[0]
            zero = s
            break

    #Zero is just missing seg3
    seg3 = list(eight - zero)[0]


    #Only missing segments 4 and 6
    seg46 = eight - set((seg0, seg1, seg2, seg3, seg5))

    #nine is the group that has exactly one out of segments 4 and 6 (seg6)
    for s in zerosixnine:
        if len(s & seg46) == 1:
            seg6 = list(s & seg46)[0]
            nine = s
            break

    #Nine is just missing seg4
    seg4 = list(eight - nine)[0]

    two = set((seg0, seg2, seg3, seg4, seg6))
    three = set((seg0, seg2, seg3, seg5, seg6))
    five = set((seg0, seg1, seg3, seg5, seg6))

    digits = [zero, one, two, three, four, five, six, seven, eight, nine]

    data_out = ""
    for s in output:
        for i in range(0,10):
            if s == digits[i]:
                data_out += str(i)

    print(data_out)
    result += int(data_out)

print(result)