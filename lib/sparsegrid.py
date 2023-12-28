from __future__ import annotations

from typing import TypeVar, Generic, Iterable, Optional
from collections.abc import Iterator
from collections import defaultdict


T = TypeVar("T")

class SparseGrid(Generic[T]):

    def __init__(self, data: Iterable[tuple[tuple[int,int],T]]):
        self.data: dict[tuple[int,int],T] = defaultdict(None)
        for pos,val in data:
            self.data[pos] = val

    def __setitem__(self, pos: tuple[int,int], val: T):
        self.data[pos] = val

    def __getitem__(self, pos: tuple[int,int]) -> Optional[T]:
        return self.data[pos]

    def __iter__(self) -> Iterator[tuple[tuple[int,int],T]]:
        return iter(self.data.items())
    
    def keys(self) -> Iterator[tuple[int,int]]:
        return iter(self.data.keys())
    
    def values(self) -> Iterator[T]:
        return iter(self.data.values())

    def boundingbox(self) -> tuple[int,int,int,int]:
        first = True
        xmin = xmax = ymin = ymax = 0

        for pos, _ in self.data.items():
            if first:
                xmin = xmax = pos[0]
                ymin = ymax = pos[1]
                first = False
                continue

            x,y = pos
            xmin = min(xmin,x)
            xmax = max(xmax,x)
            ymin = min(ymin,y)
            ymax = max(ymax,y)

        return (xmin, xmax, ymin, ymax)
    
    #Filter on value
    def filter(self, func) -> SparseGrid[T]:
        return SparseGrid([(pos, val) for pos,val in self.data.items() if func(val)])
    
    #Filter on position
    def filterPos(self, func) -> SparseGrid[T]:
        return SparseGrid([(pos, val) for pos,val in self.data.items() if func(pos)])
    
    #Map on values
    def map(self, func) -> SparseGrid[T]:
        return SparseGrid([(pos, func(val)) for pos,val in self.data.items()])
    
    #Map on positions
    def mapPos(self, func) -> SparseGrid[T]:
        return SparseGrid([(func(pos), val) for pos,val in self.data.items()])
    
    def offset(self, dx: int, dy: int) -> SparseGrid[T]:
        return self.map( lambda x,y: (x+dx, y+dy))
    
    def neighbours(self, pos: tuple[int,int]) -> Iterator[tuple[tuple[int,int],T]]:
        for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
            pos2 = pos[0]+dx,pos[1]+dy
            if pos2 in self.data: yield (pos2,self.data[pos2])

    def neighboursDiag(self, pos: tuple[int,int]) -> Iterator[tuple[tuple[int,int],T]]:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==0 and dy==0: continue
                pos2 = pos[0]+dx,pos[1]+dy
                if pos2 in self.data: yield (pos2,self.data[pos2])

    def neighboursHex(self, pos: tuple[int,int]) -> Iterator[tuple[tuple[int,int],T]]:
        for dx,dy in ( (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0)):    
            pos2 = pos[0]+dx,pos[1]+dy
            if pos2 in self.data: yield (pos2,self.data[pos2])