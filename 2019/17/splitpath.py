#!/usr/bin/env python3


pathstr = "L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,L,4,L,10,L,4,L,4,L,10,L,6,R,8,R,10,L,6,L,6,L,4,R,8,L,6,L,10,L,6,R,8,R,10,L,6,L,6,L,4,L,4,L,10"

"""
A,B,A,B,C,C,B,A,B,C
A: L,4,R,8,L,6,L,10
B: L,6,R,8,R,10,L,6,L,6
C: L,4,L,4,L,10
"""

#Try all reasonable lengths of a (max 20 chars)
for alen in range(3,21):
    A = pathstr[:alen]
    if A[-1]=="," or pathstr[alen] != ",": continue #Only end on a "full symbol"
    
    apath = pathstr.replace(A, "A")
    apath2 = apath.lstrip("A,")

    print("A: ", A, "  ", apath)

    #Try B on whatever comes after the first chunk of As
    for blen in range(3,21):
        B = apath2[:blen]
        if "A" in B: break #Gone too far!
        if B[-1]=="," or apath2[blen] != ",": continue #Only end on a "full symbol"


        bpath = apath.replace(B, "B")


        print("  B: ", B, "  ", bpath)


        #After removing all leading A's and B's, C has to be whatever is at the start up until the first A or B (minus the comma before it)
        bpath2 = bpath.lstrip("AB,")
        #maxc = min(bpath2.find("A"),bpath2.find("B")) - 1

        for clen in range(3,21):
            C = bpath2[:clen]
            if "A" in C or "B" in C: break
            if C[-1]=="," or bpath2[clen] != ",": continue #Only end on a "full symbol"
        
            if len(C) > 20: continue

            cpath = bpath.replace(C, "C")


            print("    C: ", C, "  ", cpath)

            if len(cpath) > 20: continue

            #Make sure there's only "ABC," in it
            if len(cpath.lstrip("ABC,")) > 0: continue

            #Try building original path and make sure it matches
            #origpath = cpath.replace("A",A).replace("B",B).replace("C",C)
            #if origpath == pathstr:
            print("MOVES: ", cpath)
            print("A:     ", A)
            print("B:     ", B)
            print("C:     ", C)
