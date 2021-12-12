#this is krka or mzeo or someones golfed solution that I ran just for comparison. Not mine.
import sys
a={0:1,**{int(l):0 for l in sys.stdin}}
for v in sorted(a.keys()):a[v]+=sum(a[j] for j in a if v-4<j<v)
print(max(a.values()))

