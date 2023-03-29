from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """""".split("\n")


class Solution(Puzzle):
    def __init__(self):
        super().__init__("{{{year}}}", "{{{day}}}", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [None, None])

    def solveA(self, input: list[str]) -> str | None:
        return None

    def solveB(self, input: list[str]) -> str | None:
        return None
