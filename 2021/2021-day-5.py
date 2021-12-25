from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "5", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [5, 12])

    def calculate(self, input: list[str], diagonals: bool) -> None:
        self.board = []
        for i in range(1000): self.board.append([0]*1000)
        for line in input:
            [xstart, ystart], [xend, yend] = [[int(y) for y in x.strip().split(",")] for x in line.split("->")]
            if xstart != xend and ystart != yend and not diagonals: continue
            xstep = xend - xstart
            xstep = abs(xstep) // xstep if xstep else 0
            ystep = yend - ystart
            ystep = abs(ystep) // ystep if ystep else 0
            while xstart != xend or ystart != yend:
                self.board[xstart][ystart] += 1
                xstart += xstep
                ystart += ystep
            self.board[xstart][ystart] += 1
        ans = 0
        for row in self.board:
            for col in row:
                if col >= 2: ans += 1
        return ans

    def solveA(self, input: list[str]) -> str | None:
        return self.calculate(input, False)

    def solveB(self, input: list[str]) -> str | None:
        return self.calculate(input, True)
