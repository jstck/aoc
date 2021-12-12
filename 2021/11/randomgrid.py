#!/usr/bin/env python3

import sys
import random

n, m = [int(x) for x in sys.argv[1:3]]

random.seed()

for i in range(m):
    print("".join([str(random.randint(0,9)) for j in range(n)]))