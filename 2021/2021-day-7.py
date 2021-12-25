from typing import Callable
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """16,1,2,0,4,2,7,1,2,14""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "7", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [37, 168])

    def search(self, crabs: list[int], getfuel: Callable[[list[int], int], int]) -> int:
        left = min(crabs)
        right = max(crabs)
        while left != right:
            part = (right - left) // 3
            if part == 0: return min([getfuel(crabs, loc) for loc in range(left, right+1)])
            p1 = left + part
            p2 = right - part
            f1 = getfuel(crabs, p1)
            f2 = getfuel(crabs, p2)
            if f1 > f2: left = p1
            elif f2 > f1: right = p2
            else: left += 1

    def solveA(self, input: list[str]) -> str | None:
        crabs = [int(x) for x in input[0].split(",")]
        def fuel(crabs: list[int], loc: int):
            return sum([abs(c-loc) for c in crabs])
        return self.search(crabs, fuel)

    def solveB(self, input: list[str]) -> str | None:
        crabs = [int(x) for x in input[0].split(",")]
        def fuel(crabs: list[int], loc: int):
            return sum([abs(c-loc)*(abs(c-loc)+1)//2 for c in crabs])
        return self.search(crabs, fuel)
