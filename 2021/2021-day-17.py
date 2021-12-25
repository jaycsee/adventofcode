from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """target area: x=20..30, y=-10..-5""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "17", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [45, 112])

    def parse(self, input: list[str]) -> None:
        [self.xstart, self.xend], [self.ystart, self.yend] = [x.split("..") for x in input[0].strip("targetareax=: ").split(", y=")]

    def fire(self, xpow: int, ypow: int) -> int:
        ans = 0
        x = 0
        y = 0
        while x < int(self.xend) and y > int(self.ystart):
            x += xpow
            y += ypow
            ans = max(ans, y)
            if xpow != 0: xpow -= abs(xpow) // xpow
            ypow -= 1
            if int(self.xstart) <= x <= int(self.xend) and int(self.ystart) <= y <= int(self.yend): return ans
        return None

    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        ans = 0
        for xpow in range(1, int(self.xend)+1):
            for ypow in range(int(self.ystart), 250):
                if (m := self.fire(xpow, ypow)) is not None:
                    ans = max(ans, m)
        return ans

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        ans = 0
        for xpow in range(1, int(self.xend)+1):
            for ypow in range(int(self.ystart), 250):
                if self.fire(xpow, ypow) is not None: ans += 1
        return ans
