from __future__ import annotations

from typing import TypeVar, Generic, Iterable
from collections.abc import Iterator
import itertools
#from "./sparsegrid" import SparseGrid


T = TypeVar("T")

class Grid(Generic[T]):
    
    def __init__(self, data: Iterable[Iterable[T]]):
        self.data: list[list[T]] = []
        self.size_x: int = 0
        self.size_y: int = 0
    
        
        size_x = -1
        for row in data:
            rowdata: list[T] = list(row)
            if size_x == -1:
                size_x = len(rowdata)
            else:
                assert len(rowdata)==size_x, "Different length rows in data"

            self.data.append(rowdata)

        self.size_x = size_x
        self.size_y = len(self.data)
        if self.size_y == 0: self.size_x = 0

    def __getitem__(self, pos: tuple[int,int]) -> T:
        x,y=pos
        assert 0<=x<self.size_x and 0<=y<self.size_y, f"Out of bounds: ({x}, {y})"
        return self.data[y][x]
    
    def __setitem__(self, pos: tuple[int,int], val: T):
        x,y=pos
        assert 0<=x<self.size_x and 0<=y<self.size_y, f"Out of bounds: ({x}, {y})"
        self.data[y][x] = val
    
    #Get a row or column, regular or reversed
    def row(self, y: int) -> Iterator[T]:
        return iter(self.data[y])

    def col(self, x: int) -> Iterator[T]:
        for row in self.data:
            yield row[x]

    def rowReverse(self, y: int) -> Iterator[T]:
        return reversed(list(self.row(y)))
    
    def colReverse(self, x: int) -> Iterator[T]:
        return reversed(list(self.col(x)))

    #Enumerate row or column
    def enumRow(self, y: int) -> Iterator[tuple[int,T]]:
        return enumerate(self.data[y])

    def enumCol(self, x: int) -> Iterator[tuple[int,T]]:
        for y, row in enumerate(self.data):
            yield (y,row[x])

    #Go through entire grid
    def iter(self) -> Iterator[T]:
        for y in range(self.size_y):
            for x in range(self.size_x):
                yield self[x,y]

    def enumerate(self) -> Iterator[tuple[int,int,T]]:
        for y in range(self.size_y):
            for x in range(self.size_x):
                yield x,y,self[x,y]


    def header(self) -> str:
        if self.size_x == 0 or self.size_y == 0:
            typename = "nothing"
        else:
            typename = type(self[0,0]).__name__
        return f"{self.size_x} X {self.size_y} of {typename}, {hash(self)}"

    def toString(self, separator: str = "", func=None) -> str:
        if func is None:
            func = lambda x: str(x)
        return "\n".join([separator.join([func(v) for v in row]) for row in self.data])
    
    def __str__(self) -> str:
        return self.toString()
    

    #Various transformations

    def flipY(self) -> Grid[T]:
        #Rows in reverse order
        return Grid([ self.row(y) for y in range(self.size_y-1, -1, -1) ])
    
    def flipX(self) -> Grid[T]:
        #Reverse each row
        return Grid([self.rowReverse(y) for y in range(self.size_y)])


    def transpose(self) -> Grid[T]:
        #Create grid with columns as rows
        return Grid([self.col(x) for x in range(self.size_x)])

    def rotateCW(self) -> Grid[T]:
        #New row = column reversed
        return Grid([self.colReverse(x) for x in range(self.size_x)])
        
    def rotateCCW(self) -> Grid[T]:
        #New row = columns in reverse order
        return Grid([self.col(x) for x in range(self.size_x-1, -1, -1)])
    
    def rotate180(self) -> Grid[T]:
        return Grid([ self.rowReverse(y) for y in range(self.size_y-1, -1, -1) ])


    def __hash__(self):
        #Tuple of all rows as tuples. Assumes T is hashable.
        return hash(tuple(tuple(row) for row in self.data))

    def __eq__(self, other: Grid[T]) -> bool:
        if self.size_x != other.size_x or self.size_y != other.size_y:
            return False
        
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self[x,y] != other[x,y]:
                    return False

        return True
    
    def copy(self) -> Grid[T]:
        #__init__ will copy all data to new list of new lists. Elements themselfs are not deepcopied
        return Grid(self.data)
    
    def map(self, func) -> Grid:
        return Grid( [ map(func, row) for row in self.data ] )
    
    def appendX(self, other: Grid[T]) -> Grid[T]:
        assert self.size_y == other.size_y
        return Grid([itertools.chain(self.row(y), other.row(y)) for y in range(self.size_y)])
    
    def appendY(self, other: Grid[T]) -> Grid[T]:
        assert self.size_x == other.size_x
        return Grid(self.data + other.data)
    
    def neighbours(self, x: int, y: int) -> Iterator[tuple[int,int,T]]:
        for dx, dy in ((-1,0), (1,0), (0,-1), (0,1)):
            x1,y1 = x+dx,y+dy
            if x1<0 or x1>=self.size_x or y1<0 or y1>=self.size_y:
                continue
            yield (x1,y1,self[x1,y1])

    def neighboursDiag(self, x: int, y: int) -> Iterator[tuple[int,int,T]]:
        for dx in (-1,0,1):
            x1 = x+dx
            if x1<0 or x1>=self.size_x: continue
            for dy in (-1,0,1):
                if dx==0 and dy==0: continue
                y1 = y+dy
                if y1<0 or y1>=self.size_y: continue
                
                yield (x1,y1,self[x1,y1])

    #Create a sparse grid with a filter on value
#    def sparseGrid(self, filter=None) -> SparseGrid[T]:
#        if filter is None:
#            filter = lambda x: True
#
#        return SparseGrid( ((x,y),val) for (x,y,val) in self.enumerate() if filter(val) )
        


if __name__ == "__main__":
    griddle = [ [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    #griddle = [ "abc", "def", "ghi", "jkl" ]
    g = Grid(griddle)

    f = g.copy()

    f[1,1] = 99

    print(g==f)

    print(g.header())
    print(g)
    print()
    print(f.header())
    print(f.toString(", "))

