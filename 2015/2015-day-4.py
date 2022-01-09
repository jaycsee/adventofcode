from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

import hashlib

given = """abcdef""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2015", "4", timeout=30, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [609043, None])

    def solveA(self, input: list[str]) -> str | None:
        i = 0
        while True:
            if hashlib.md5((input[0] + str(i)).encode("ascii")).hexdigest().startswith("00000"): return i
            i += 1

    def solveB(self, input: list[str]) -> str | None:
        i = 0
        while True:
            if hashlib.md5((input[0] + str(i)).encode("ascii")).hexdigest().startswith("000000"): return i
            i += 1