from collections import defaultdict
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """abc

a
b
c

ab
ac

a
a
a
a

b""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "6", timeout=5, sanitized_input=False)

    def test(self) -> bool:
        return self.expect(given, [11, 6])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        group = set()
        for line in input:
            line = line.strip("\n ")
            if not line: 
                ans += len(group)
                group = set()
            for x in line.strip("\n "):
                group.add(x)
        ans += len(group)
        return ans

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        group = defaultdict(int)
        n = 0
        for line in input:
            if not line.strip(): 
                for k,v in group.items():
                    if v == n: ans += 1
                n = 0
                group = defaultdict(int)
                continue
            for x in line.strip("\n "): 
                group[x] += 1
            n += 1
        for k,v in group.items():
            if v == n: 
                ans += 1
        return ans
