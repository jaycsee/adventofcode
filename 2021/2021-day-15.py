from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "15", timeout=30, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [40, 315])
    
    def parse(self, input: list[str]) -> None:
        self.grid = []
        self.min = []
        for line in input: 
            self.grid.append([int(x) for x in line])
            self.min.append([None] * len(line))

    def getGrid(self, x: int, y: int) -> int | None:
        if not (0 <= x < len(self.grid)) or not (0 <= y < len(self.grid[0])): return None
        return self.grid[x][y]

    def getMin(self, x: int, y: int) -> int | None:
        if not (0 <= x < len(self.grid)) or not (0 <= y < len(self.grid[0])): return None
        return self.min[x][y]

    def computeLowest(self, x: int, y: int) -> set[tuple[int, int]]:
        if not (0 <= x < len(self.grid)) or not (0 <= y < len(self.grid[0])): return set()
        l = [self.getMin(x+1, y), self.getMin(x-1, y), self.getMin(x, y+1), self.getMin(x, y-1)]
        l = [x for x in l if x is not None]
        if len(l) == 0: return
        m = min(l) + self.getGrid(x, y)
        if self.getMin(x, y) is None or self.getMin(x, y) > m:
            self.min[x][y] = m
            r = set()
            r.add((x+1, y))
            r.add((x-1, y))
            r.add((x, y+1))
            r.add((x, y-1))
            return r
        return set()

    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        self.min[0][0] = 0
        r = set([(1, 0), (0, 1)])
        n = set()
        while r:
            n = set()
            for x, y in r: 
                for v in self.computeLowest(x, y):
                    n.add(v)
            r = n
        return self.min[-1][-1]

    def solveB(self, input: list[str]) -> str | None:
        newin = []
        for line in input:
            l = []
            for x in range(5):
                for i in line:
                    v = (int(i) + x)
                    if v > 9: v -= 9
                    l.append(v)
            newin.append(l)
        input = []
        for x in range(5):
            l = []
            for line in newin: 
                n = []
                for i in line:
                    v = (int(i) + x)
                    if v > 9: v -= 9
                    n.append(v)
                l.append(n)
            input.extend(l)
        self.parse(input)
        self.min[0][0] = 0
        r = set([(1, 0), (0, 1)])
        n = set()
        while r:
            n = set()
            for x, y in r: 
                for v in self.computeLowest(x, y):
                    n.add(v)
            r = n
        return self.min[-1][-1]