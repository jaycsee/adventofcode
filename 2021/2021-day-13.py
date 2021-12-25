from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

fold along y=7
fold along x=5""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "13", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [17, None])

    def parse(self, input: list[str]) -> None:
        self.grid = []
        for line in range(2000):
            l = [False] * 2000
            self.grid.append(l)
        for line in input:
            if line.startswith("fold"):
                break
            x, y = line.split(",")
            x, y = int(x), int(y)
            self.grid[y][x] = True
    
    def fold(self, inst: str) -> None:
        if not inst.startswith("fold"): return
        inst, val = inst.split("=")
        if inst.endswith("x"):
            val = int(val)
            offset = 1
            while val - offset >= 0 and val + offset < len(self.grid[0]):
                for i in range(len(self.grid)):
                    self.grid[i][val - offset] |= self.grid[i][val + offset]
                    self.grid[i][val + offset] = False
                offset += 1
        else:
            val = int(val)
            offset = 1
            while val - offset >= 0 and val + offset < len(self.grid):
                for i in range(len(self.grid[0])):
                    self.grid[val - offset][i] |= self.grid[val + offset][i]
                    self.grid[val + offset][i] = False
                offset += 1


    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        for line in input:
            if not line.startswith("fold"): continue
            self.fold(line)
            break
        ans = 0
        for line in self.grid:
            for val in line:
                ans += val
        return ans

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        for line in input:
            self.fold(line)

        for line in self.grid[:6]:
            print("".join(["#" if line[x] else "." for x in range(60)]))