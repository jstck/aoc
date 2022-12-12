class Grid:

    def __init__(self, sizeX, sizeY, defaultValue=None):
        self.sizeX = sizeX
        self.sizeY = sizeY

        self._grid=[]
        for y in range(sizeY):
            if callable(defaultValue):
                row = [defaultValue(x, y) for x in range(sizeX)]
            else:
                row = [defaultValue] * sizeX
            self._grid.append(row)

    def __getitem__(self, arg):
        if isinstance(arg, int):
            #Get a row
            return self._grid[arg]
        elif isinstance(arg, tuple) and len(arg)==2:
            #Get a cell
            (x,y) = arg
            return self._grid[y][x]
        else:
            raise(IndexError("INVALID DIMENSIONS"))

    def __setitem__(self, arg, value):
        if isinstance(arg, int):
            #Set a row
            if len(value) != self.sizeX:
                raise IndexError(f"Invalid row size: {len(value)}, must be {self.sizeX}")
            self._grid[arg] = value
        elif isinstance(arg, tuple) and len(arg)==2:
            #Set a cell
            (x,y) = arg
            self._grid[y][x] = value
        else:
            raise(IndexError("INVALID DIMENSIONS"))

    def __str__(self):
        result = ""
        for row in self._grid:
            result += "".join([str(cell) for cell in row]) + "\n"
        return result
    
    def __repr__(self):
        return repr(self._grid)

    def row(self, y):
        return self._grid[y]

    def col(self, x):
        return [self._grid[y][x] for y in range(self.sizeY)]

    def rows(self):
        return iter(self._grid)

    def cols(self):
        for x in range(self.sizeX):
            yield self.col(x)

    def transpose(self):
        t = Grid(0,0)
        t.sizeX = self.sizeY
        t.sizeY = self.sizeX
        for r in self.cols():
            t._grid.append(r)
        return t