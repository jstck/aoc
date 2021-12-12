#!/usr/bin/env python3

import sys

current = set()

required = set(["byr","iyr","eyr","hgt","hcl","ecl","pid"])

valids = 0

ln = 0

for line in sys.stdin:
    line = line.strip()
    ln += 1
    if len(line)>0:

    
        pairs = line.split()
        for pair in pairs:
            (key, value) = pair.split(":", 1)
            if key in required:
                current.add(key) #Only add "valid fields"
            else:
                print("Line", ln, "found", key, ", ignored")

    else:

        print("Finished passport at line", ln)

        #End of current data chunk, validate it
        if len(required - current) == 0:
            print("valid")
            valids += 1
        else:
            print("invalid", current, "missing", required-current)

        print()
        
        #Fresh passport
        current = set()
    
print(valids)