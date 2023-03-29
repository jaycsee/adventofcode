from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "4", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["2", "4"])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        for s in input:
            (s1, e1), (s2, e2) = [x.split("-") for x in s.split(",")]
            s1 = int(s1)
            e1 = int(e1)
            s2 = int(s2)
            e2 = int(e2)
            if (s1 <= s2 and e2 <= e1) or (s2 <= s1 and e1 <= e2):
                ans += 1
        return str(ans)

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        for s in input:
            (s1, e1), (s2, e2) = [x.split("-") for x in s.split(",")]
            s1 = int(s1)
            e1 = int(e1)
            s2 = int(s2)
            e2 = int(e2)
            if not (s1 <= e1 < s2 <= e2 or s2 <= e2 < s1 <= e1) :
                ans += 1
        return str(ans)
