from __future__ import annotations
from typing import Iterable

class IntervalSet():
    def __init__(self):
        self.data: list[tuple[int,int]] = []

    def intervals(self) -> Iterable[tuple[int,int]]:
        return iter(self.data)
    

    #Check if two ranges overlap
    @staticmethod
    def overlaps(r1: tuple[int,int], r2: tuple[int,int]) -> bool:
        a1, b1 = r1
        a2, b2 = r2

        if a1 >= a2 and a1 <= b2: return True
        if b1 >= a2 and b1 <= b2: return True
        if a2 >= a1 and a2 <= b1: return True
        if b1 >= a2 and b1 <= b2: return True
        return False
        
    #Merge two ranges (assumed to overlap)
    @staticmethod
    def merge(r1: tuple[int,int], r2: tuple[int,int]) -> tuple[int,int]:
        a1, b1 = r1
        a2, b2 = r2

        a = min(a1,a2)
        b = max(b1,b2)

        return (a,b)

    #Add an interval. If it overlaps with another one, remove that, merge them and repeat
    def add(self, interval: tuple[int,int]):
        for i in range(len(self.data)):
            e = self.data[i]

            if self.overlaps(interval,e):
                merged = self.merge(interval, e)
                del self.data[i]
                return self.add(merged) #Attempt at TCO
            
        self.data.append(interval)
            
    def contains(self, x: int) -> bool:
        for (a,b) in self.data:
            if a<=x and x<=b:
                return True
        return False


