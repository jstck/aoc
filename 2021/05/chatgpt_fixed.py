#!/usr/bin/env python3
# Store the coordinates of the line segments in a set
coords = set()

# Read the input and add the coordinates to the set
with open("sample") as f:
    for line in f:
        a, b = line.strip().split("->")
        x1, y1= map(int, a.strip().split(","))
        x2, y2= map(int, b.strip().split(","))
        coords.add((x1, y1))
        coords.add((x2, y2))

# Count the number of points where at least two lines overlap
count = 0
for x, y in coords:
    if (x, y) in coords:
        count += 1

# Print the result
print(count)

