from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

from collections import Counter

given = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "2", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [2, 1])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        for line in input:
            policy, password = line.split(": ")
            mino, maxo, letter = policy.replace("-", " ").split(" ")
            if int(mino) <= Counter(password)[letter] <= int(maxo): ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        for line in input: 
            policy, password = line.split(": ")
            pos1, pos2, letter = policy.replace("-", " ").split(" ")
            if (password[int(pos1)-1] == letter) ^ (password[int(pos2)-1] == letter): ans += 1
        return ans
