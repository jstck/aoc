from __future__ import annotations

import math
import sys
from typing import List, Union, Tuple, TypeAlias, Generator
import copy

TextGrid: TypeAlias = List[List[str]]

def chunks(input: list[str], ints: bool=False) -> list[list[str]]:
    chunk = []
    chunky = []
    for line in input:
        if len(line) == 0:
            chunky.append(chunk)
            chunk = []
        else:
            if ints:
                chunk.append(int(line))
            else:
                chunk.append(line)

    if len(chunk)>0:
        chunky.append(chunk)
    return chunky

class Tile:
    SIZE=10

    TOP=0
    RIGHT=1
    BOTTOM=2
    LEFT=3

    flips: List[Union[int,None]] = [None] * 2**SIZE

    @staticmethod
    def flipedge(x: int) -> int:
        f = Tile.flips[x]
        if f is not None:
            return f
        
        bits = bin(x)[2:]

        #Reverse bits and pad to 10 digits
        newbits = '0b' + bits[::-1] + '0'*(Tile.SIZE-len(bits))
        y = int(newbits, 2)
        Tile.flips[x] = y
        Tile.flips[y] = x
        return y


    @staticmethod
    def _strtoedge(s: str) -> int:
        if len(s) != Tile.SIZE:
            print("INVALID TILE SIZE: ", s)
        bits = "0b" + s.replace(".", "0").replace("#","1")
        return int(bits, 2)

    @staticmethod
    def fromInput(data: List[str]) -> Tile:
        header = data.pop(0)
        id = int(header.split()[1][:-1])

        #Edges are encoded as ints (with .=0 and #=1 read as binary), left-to-right or top-to-bottom.
        top = Tile._strtoedge(data[0].strip())
        bottom = Tile._strtoedge(data[-1].strip())
        left = Tile._strtoedge("".join([line.strip()[0] for line in data]))
        right = Tile._strtoedge("".join([line.strip()[-1] for line in data]))

        edges = [top, right, bottom, left]
        rotation = 0
        mirrored = False

        #Text content in tile (minus border)
        contents = [list(line[1:-1]) for line in data[1:-1]]

        return Tile(id, edges, rotation, mirrored, contents)

    def __init__(self, id: int, edges: List[int], rotation: int, mirrored: bool, contents: TextGrid):
        self.id = id
        self.edges = edges
        self.rotation = rotation % 4
        self.mirrored = mirrored
        self.contents = contents

        #Mirrored version of edges (along Y axis)
        #Top and bottom get flipped
        #Left and right get swapped
        self.mirrored_edges = [
            Tile.flipedge(edges[Tile.TOP]),
            edges[Tile.LEFT],
            Tile.flipedge(edges[Tile.BOTTOM]),
            edges[Tile.RIGHT]
        ]

    def getId(self) -> int:
        return self.id

    def getEdge(self, edge: int) -> int:
    
        [a, b, c, d] = self.edges
        [a1, b1, c1, d1] = map(Tile.flipedge, self.edges)

        if not self.mirrored:
            if self.rotation == 0:
                return self.edges[edge]
            elif self.rotation == 1:
                return [d1, a, b1, c][edge]
            
            #Everything is inverted from initial state
            elif self.rotation == 2:
                return [c1, d1, a1, b1][edge]
            
            elif self.rotation == 3:
                return [b, c1, d, a1][edge]
    
        else: #Mirrored
            if self.rotation == 0:
                return [a1, d, c1, b][edge]
            elif self.rotation == 1:
                return [b1, a1, d1, c1][edge]
            elif self.rotation == 2:
                return [c, b1, a, d1][edge]
            elif self.rotation == 3:
                return [d, c, b, a][edge]
            
        print("INVALID TILE STATE!!!!")
        print("Edge", edge)
        print(self)
        sys.exit(1)

        
    def mirror(self) -> Tile:
        return Tile(self.id, self.edges, self.rotation, not self.mirrored, self.contents)
    
    def rotate(self) -> Tile:
        return Tile(self.id, self.edges, (self.rotation+1)%4, self.mirrored, self.contents)
    
    def rotate2(self) -> Tile:
        return Tile(self.id, self.edges, (self.rotation+2)%4, self.mirrored, self.contents)
    
    def rotate3(self) -> Tile:
        return Tile(self.id, self.edges, (self.rotation+3)%4, self.mirrored, self.contents)
    
    def getContents(self) -> TextGrid:
        grid = []
        for row in self.contents:
            grid.append(list(row))

        if self.mirrored:
            grid = mirror_grid(grid)

        if self.rotation > 0:
            grid = rotate_grid(grid, self.rotation)

        return grid
    
    def __repr__(self) -> str:
        u = self.getEdge(Tile.TOP)
        r = self.getEdge(Tile.RIGHT)
        d = self.getEdge(Tile.BOTTOM)
        l = self.getEdge(Tile.LEFT)
        if self.mirrored:
            m="m"
        else:
            m="r"
        ro = self.rotation

        s = f"""+----{u:4d}----+
|            |
{l:<4d}         |
|  {self.id:4d}{m}{ro}    |
|         {r:4d}
|            |
+----{d:4d}----+
{self.edges}
{self.mirrored_edges}
"""
        return s
    
    def __str__(self) -> str:
        return self.__repr__()
    
TileGrid: TypeAlias = list[list[Tile]]

def copygrid(grid: TileGrid) -> TileGrid:
    #Moderately shallow copy (keep references to actual tile objects as they are)
    return [row.copy() for row in grid]

def rotate_grid(grid: List, rotations: int = 1) -> List:
    rotations = rotations % 4

    if rotations == 0:
        return grid
    
    if rotations == 1:
        size = len(grid)

        """
        1 2 3
        4 5 6
        7 8 9
        =>
        7 4 1
        8 5 2
        9 6 3
        """

        newgrid = []
        for y in range(size):
            newrow = []
            for x in range(size):
                newrow += [(grid[size-x-1][y])]
            newgrid.append(newrow)
        return newgrid

    if rotations == 2:
        #Mirror along both X and Y -> two rotations
        newgrid = mirror_grid(grid)
        newgrid.reverse()
        return newgrid

    if rotations == 3:
        size = len(grid)



        """
        1 2 3
        4 5 6
        7 8 9
        =>
        3 6 9
        2 5 8
        1 4 7
        """

        newgrid = []
        for y in range(size):
            newrow = []
            for x in range(size):
                newrow += [(grid[x][size-y-1])]
            newgrid.append(newrow)
        return newgrid
        
    raise ValueError


def mirror_grid(grid: TextGrid) -> TextGrid:
    newgrid = []

    for line in grid:
        newline = line.copy()
        newline.reverse()
        newgrid.append(newline)

    return newgrid


def makemoves(grid, tiles: List[Tile], tilesused: List[int], nexttile: Tuple[int,int]) -> Union[TileGrid,None]:
    gridsize = len(grid)

    edge_above = None
    edge_left = None

    (x, y) = nexttile

    if x > 0:
        edge_left = grid[y][x-1].getEdge(Tile.RIGHT)
    if y > 0:
        edge_above = grid[y-1][x].getEdge(Tile.BOTTOM)

    for tile in tiles:
        #Skip already used tiles
        if tile.getId() in tilesused:
            continue

        mirror = tile.mirror()
        alltiles = [tile, tile.rotate(), tile.rotate2(), tile.rotate3(), mirror, mirror.rotate(), mirror.rotate2(), mirror.rotate3()]

        solution = None

        for newtile in alltiles:
            if edge_left is not None and newtile.getEdge(Tile.LEFT) != edge_left:
                continue
            if edge_above is not None and newtile.getEdge(Tile.TOP) != edge_above:
                continue

            newgrid = copygrid(grid)
            newgrid[y][x] = newtile
            
            x1 = x + 1
            if x1 >= gridsize:
                y1=y+1
                x1=0
            else:
                y1=y

            if y1>=gridsize:
                #Found a solution!!
                print("Solution found!")

                return newgrid

            #Keep searching
            result = makemoves(newgrid, tiles, tilesused + [newtile.getId()], (x1, y1))
            
            #Stop if solution found (it will return multiple, all rotations and mirrors of each other)
            if result is not None:
                return result
    return None
    

def part1(input: list[str]):
    tiles: List[Tile] = []
    tileids: List[int] = []
    for tilelines in chunks(input):
        tile = Tile.fromInput(tilelines)
        tiles.append(tile)
        tileids.append(tile.getId())

    print(tileids)
    ntiles = len(tiles)

    gridsize = int(math.sqrt(ntiles))
    if gridsize*gridsize != ntiles:
        print(ntiles, "NOT A SQUARE GRID!!")
    else:
        print(f"{ntiles} tiles, {gridsize} X {gridsize}")


    grid = [[None] * gridsize for _ in range(gridsize)]

    solution = makemoves(grid, tiles, [], (0,0))

    if solution is None:
        print("No solution found!")
        return (0, None)

    tl = solution[0][0].getId()
    tr = solution[0][gridsize-1].getId()
    bl = solution[gridsize-1][0].getId()
    br = solution[gridsize-1][gridsize-1].getId()
    print(f"{tl:4}  {tr:4}")
    print(f"{bl:4}  {br:4}")
    result = tl*tr*bl*br
    print(result)

    return (result, solution)
    
def printgrid(grid: TextGrid):
    for row in grid:
        print("".join(row))

#Join a list of textgrids into one horizontal chunk (vertically they can just be concatenated)
def joingrids(grids: List[TextGrid]) -> TextGrid:
    newgrid = []

    for row in range(len(grids[0])):
        newrow = []
        for subgrid in grids:
            newrow += subgrid[row]
        newgrid.append(newrow)
    return newgrid

def makeallgrids(grid: TextGrid) -> Generator[TextGrid, None, None]:
    yield grid
    yield rotate_grid(grid, 1)
    yield rotate_grid(grid, 2)
    yield rotate_grid(grid, 3)

    grid = mirror_grid(grid)
    yield(grid)
    yield rotate_grid(grid, 1)
    yield rotate_grid(grid, 2)
    yield rotate_grid(grid, 3)


seamonster_raw: str = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n")

seamonster: TextGrid = [list(row) for row in seamonster_raw.split("\n")]


def findseamonsters(grid: TextGrid) -> Tuple[int, TextGrid]:
    grid = copy.deepcopy(grid)
    size_x = len(grid[0])
    size_y = len(grid)

    monster_x = len(seamonster[0])
    monster_y = len(seamonster)

    monsters = 0

    for y in range(size_y - monster_y):
        for x in range(size_x - monster_x):
            
            #Search for a monster in current position
            match = True
            for my in range(monster_y):
                for mx in range(monster_x):
                    if seamonster[my][mx] == "#" and grid[y+my][x+mx] != "#": # not in ["#", "O"]:
                        match = False
                        break
                if not match:
                    break

            #Should monsters here be marked / removed?
            if match:
                print(f"Found match at X={x} Y={y}")
                monsters += 1
                for my in range(monster_y):
                    for mx in range(monster_x):
                        if seamonster[my][mx] == "#":
                            grid[y+my][x+mx] = "O"

    print(f"Found {monsters} sea monsters")
    return (monsters, grid)
            

def sea_roughness(grid: TextGrid) -> int:
    rough = 0
    for row in grid:
        rough += len([x for x in row if x=="#"])
    return rough
            
def part2(solution: Union[None,TileGrid] = None) -> int:
    if solution is None:
        return 0
    
    grid = []
    min_roughness = 100000000000

    #Make a massive text grid out of all the tiles
    for tilerow in solution:
        chunk = []
        for tile in tilerow:
            chunk.append(tile.getContents())

        grid += joingrids(chunk)

    for grid in makeallgrids(grid):
        monsters, grid = findseamonsters(grid)

        if monsters > 0:
            printgrid(grid)
        roughness = sea_roughness(grid)
        print(f"Roughness: {roughness}")
        min_roughness = min(min_roughness, roughness)

    return min_roughness
