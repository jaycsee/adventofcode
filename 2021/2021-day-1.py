from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

given = """199
200
208
210
200
207
240
269
260
263""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "1", timeout=10, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [7, 5])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        for i in range(1, len(input)):
            if int(input[i]) > int(input[i-1]): ans += 1
        return ans
        
    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        for i in range(3, len(input)):
            if int(input[i]) > int(input[i-3]): ans += 1
        return ans
        