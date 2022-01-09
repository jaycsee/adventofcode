from functools import reduce
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "3", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [7, 336])

    def runSlope(self, right: int, down: int) -> int: 
        ans = 0
        x = 0
        for line in self.grid[down::down]:
            x += right
            x %= len(line) 
            if line[x] == "#": ans += 1
        return ans

    def solveA(self, input: list[str]) -> str | None:
        self.grid = []
        for line in input:
            self.grid.append(list(line))
        return self.runSlope(3, 1)

    def solveB(self, input: list[str]) -> str | None:
        self.grid = []
        for line in input:
            self.grid.append(list(line))
        return reduce(lambda x,y: x*y, [self.runSlope(1, 1), self.runSlope(3, 1), self.runSlope(5, 1), self.runSlope(7, 1), self.runSlope(1, 2)])
