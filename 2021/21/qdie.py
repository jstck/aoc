#Number of each outcome for 3d3
splits = {}

for i in [1,2,3]:
  for j in [1,2,3]:
    for k in [1,2,3]:
      sum = i+j+k
      splits[sum] = 1 + splits.get(sum,0)

print(splits)