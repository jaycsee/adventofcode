from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

from collections import deque

given = """3,4,3,1,2""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "6", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [5934, 26984457539])
    
    def calc(self, input: list[str], days: int) -> None:
        timer = [0]*7
        for x in input[0].split(","): timer[int(x)] += 1
        timer = deque(timer)
        newtimer = deque([0]*9)
        for _ in range(days):
            new = timer[0] + newtimer[0]
            timer[0] += newtimer[0]
            newtimer[0] = new
            timer.rotate(-1)
            newtimer.rotate(-1)
        return sum(timer) + sum(newtimer)

    def solveA(self, input: list[str]) -> str | None:
        return self.calc(input, 80)

    def solveB(self, input: list[str]) -> str | None:
        return self.calc(input, 256)
