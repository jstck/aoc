#!/usr/bin/env python3

import sys
import re

allanswers = []

sum = 0
ln=0

for line in sys.stdin:
    line = line.strip()
    ln += 1
    if not re.match("^[a-z]*$", line):
        print("STRANGE RESPONSE", line)
    if len(line)==0:

        answers = set.intersection(*allanswers)

        #End of current data chunk
        count = len(answers)

        sum += count

        print("Finished group at line", ln, answers, count, sum)
        
        #Fresh group
        allanswers = []
    else:
        print(line)
        oneguy = set(list(line))
        
        allanswers.append(oneguy)

    
    
print(sum)