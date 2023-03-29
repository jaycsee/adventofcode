from functools import cmp_to_key

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "13", timeout=5, sanitized_input=False)

    def test(self) -> bool:
        return self.expect(given, ["13", "140"])

    def check(self, left, right) -> bool | None:
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            elif right < left:
                return False
            else:
                return None
        elif isinstance(left, list) and isinstance(right, list):
            for l, r in zip(left, right):
                result = self.check(l, r)
                if result is False or result is True:
                    return result
            if len(left) < len(right):
                return True
            elif len(right) < len(left):
                return False
            else:
                return None
        else:
            if isinstance(left, int):
                left = [left]
            if isinstance(right, int):
                right = [right]
            return self.check(left, right)

    def solveA(self, input: list[str]) -> str | None:
        pairs = "\n".join([x.strip() for x in input]).split("\n\n")
        ans = 0
        for i, pair in enumerate(pairs):
            i += 1
            left, right = pair.split("\n")
            correct = self.check(eval(left), eval(right))
            if correct:
                ans += i
        return str(ans)

    def solveB(self, input: list[str]) -> str | None:
        input = [x for x in self.sanitize(input) if x]

        p1 = [[2]]
        p2 = [[6]]

        ans1 = 1
        ans2 = 2
        for p in input:
            if self.check(p1, eval(p)) is False:
                ans1 += 1
            if self.check(p2, eval(p)) is False:
                ans2 += 1

        return str(ans1 * ans2)
