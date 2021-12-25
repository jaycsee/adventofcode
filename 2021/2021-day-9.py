from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "9", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [15, 1134])

    def solveA(self, input: list[str]) -> str | None:
        grid = []
        for line in input: 
            grid.append([int(x) for x in line])
        ans = 0
        for i, line in enumerate(grid):
            for j, val in enumerate(line):
                low = True
                if (0 <= i+1 < len(grid)): low &= val < grid[i+1][j]
                if (0 <= i-1 < len(grid)): low &= val < grid[i-1][j]
                if (0 <= j+1 < len(grid[i])): low &= val < grid[i][j+1]
                if (0 <= j-1 < len(grid[i])): low &= val < grid[i][j-1]
                if low: ans += val + 1
        return ans
        

    def solveB(self, input: list[str]) -> str | None:
        grid = []
        mark = []
        for line in input: 
            grid.append([int(x) for x in line])
            mark.append([False] * len(line))
        sizes = []
        def search(x: int, y: int) -> int:
            if not (0 <= x < len(grid)) or not (0 <= y < len(grid[0])): return 0
            if mark[x][y] or grid[x][y] == 9: return 0
            mark[x][y] = True
            return search(x+1, y) + search(x-1, y) + search(x, y+1) + search(x, y-1) + 1
        for i, line in enumerate(grid):
            for j, val in enumerate(line):
                low = True
                if (0 <= i+1 < len(grid)): low &= val < grid[i+1][j]
                if (0 <= i-1 < len(grid)): low &= val < grid[i-1][j]
                if (0 <= j+1 < len(grid[i])): low &= val < grid[i][j+1]
                if (0 <= j-1 < len(grid[i])): low &= val < grid[i][j-1]
                if low: sizes.append(search(i, j))
        sizes.sort(reverse=True)
        return sizes[0] * sizes[1] * sizes[2]