#!/usr/bin/env python3

import sys, re

current = set()

required = set(["byr","iyr","eyr","hgt","hcl","ecl","pid"])

valids = 0

ln = 0

def isvalid(key, value):
    try:
        if key == "byr":
            return int(value) >= 1920 and int(value) <= 2002
        if key == "iyr":
            return int(value) >= 2010 and int(value) <= 2020
        if key == "eyr":
            return int(value) >= 2020 and int(value) <= 2030
        if key == "hgt":
            unit=value[-2:]
            height=int(value[:-2])
            if unit=="cm":
                return height >= 150 and height <= 193
            if unit=="in":
                return height >= 59 and height <= 76
            return False
        if key == "hcl":
            return bool(re.match(r'^#[0-9a-f]{6}$', value))
        if key == "ecl":
            return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        if key == "pid":
            return bool(re.match(r'^\d{9}$', value))
        if key == "cid":
            return True
    except ValueError:
        print("Bonkers data:", key, value)
        return False

    return False

for line in sys.stdin:
    line = line.strip()
    ln += 1
    if len(line)==0:

        #print("Finished passport at line", ln)

        #End of current data chunk, validate it
        if len(required - current) == 0:
            #print("valid")
            valids += 1
        else:
            #print("invalid", current, "missing", required-current)
            pass

        print()
        
        #Fresh passport
        current = set()
    
    pairs = line.split()
    for pair in pairs:
        (key, value) = pair.split(":", 1)
        value=value.strip()
        if key in required and isvalid(key, value):
            current.add(key) #Only add "valid fields"
        else:
            print("Line", ln, "found", key, ":", value, ", ignored")

print(valids)