#!/usr/bin/env python3

import sys

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

    #Could remove duplicates here, but sets are not hashable so meh

    #Known digits
    one = [ d for d in alldigits if len(d)==2 ][0]
    four = [ d for d in alldigits if len(d)==4 ][0]
    seven = [ d for d in alldigits if len(d)==3 ][0]
    eight = set(list("abcdefg"))

    #Top segment is in 7 but not 1
    seg0 = list(seven - one)[0]

    #Zeroes, sixes and nines all have 6 elements
    zerosixnine = [ d for d in alldigits if len(d)==6 ]

    #Six is the 6-segment group that has exactly one intersecting segment with one (2&5)
    for s in zerosixnine:
        if len(s & one) == 1:
            seg5 = list(s & one)[0]
            six = s
            break

    #Six is just missing seg2
    seg2 = list(eight - six)[0]

    #Segments in 4 but not 1
    seg13 = four - one

    #zero is the group that has exactly one out of segments 1 and 3 (seg1)
    for s in zerosixnine:
        if len(s & seg13) == 1:
            seg1 = list(s & seg13)[0]
            zero = s
            break

    #Zero is just missing seg3
    seg3 = list(eight - zero)[0]

    #Only missing segments 4 and 6 now
    seg46 = eight - set((seg0, seg1, seg2, seg3, seg5))

    #nine is the group that has exactly one out of segments 4 and 6 (seg6)
    for s in zerosixnine:
        if len(s & seg46) == 1:
            seg6 = list(s & seg46)[0]
            nine = s
            break

    #Nine is just missing seg4
    seg4 = list(eight - nine)[0]

    #All the segments are known, construct the remaining digits
    two = set((seg0, seg2, seg3, seg4, seg6))
    three = set((seg0, seg2, seg3, seg5, seg6))
    five = set((seg0, seg1, seg3, seg5, seg6))

    digits = [zero, one, two, three, four, five, six, seven, eight, nine]

    #Match each output to the correct digit
    data_out = ""
    for s in output:
        for i in range(0,10):
            if s == digits[i]:
                data_out += str(i)

    #print(data_out)
    result += int(data_out)

print(result)