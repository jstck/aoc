#!/usr/bin/env python3

import sys

answers = set()

sum = 0
ln=0

for line in sys.stdin:
    line = line.strip()
    ln += 1
    if len(line)==0:

        #End of current data chunk
        count = len(answers)

        sum += count

        print("Finished group at line", ln, count, sum)
        
        #Fresh group
        answers = set()
    else:
        answers.update(list(line))

    
    
print(sum)