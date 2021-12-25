from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "11", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [1656, 195])

    def inc(self, i: int, j: int) -> None:
        if not (0 <= i < len(self.new)):
            return
        if not (0 <= j < len(self.new[i])):
            return
        if self.new[i][j] == 0 or (i, j) in self.flashed:
            return
        self.new[i][j] += 1

    def check(self, i: int, j: int) -> None:
        if not (0 <= i < len(self.new)):
            return False
        if not (0 <= j < len(self.new[i])):
            return False
        return self.new[i][j] > 9

    def flash(self, i: int, j: int) -> None:
        if not (0 <= i < len(self.new)):
            return
        if not (0 <= j < len(self.new[i])):
            return
        if self.new[i][j] == 0 or (i, j) in self.flashed:
            return
        self.flashed.add((i, j))
        self.new[i][j] = 0
        for io in range(-1, 2):
            for jo in range(-1, 2):
                self.inc(i + io, j + jo)
                if self.check(i + io, j + jo):
                    self.flash(i + io, j + jo)

    def solveA(self, input: list[str]) -> str | None:
        self.new = []
        self.old = [[int(x) for x in line] for line in input]
        ans = 0
        c = 0
        for _ in range(100):
            self.new = [[x + 1 for x in line] for line in self.old]
            self.flashed = set()
            for i, line in enumerate(self.new):
                for j, v in enumerate(line):
                    if self.check(i, j): self.flash(i, j)
            self.old = self.new
            ans += len(self.flashed)
        return ans

    def solveB(self, input: list[str]) -> str | None:
        self.new = []
        self.old = [[int(x) for x in line] for line in input]
        ans = 0
        c = 0

        while True:
            self.new = [[x + 1 for x in line] for line in self.old]
            self.flashed = set()
            for i, line in enumerate(self.new):
                for j, v in enumerate(line):
                    if self.check(i, j): self.flash(i, j)
            self.old = self.new
            if len(self.flashed) == (len(self.new) * len(self.new[0])):
                ans = c + 1
                break
            else:
                c += 1
        return ans

