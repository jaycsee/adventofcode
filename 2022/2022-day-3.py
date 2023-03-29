from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "3", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["157", "70"])

    def solveA(self, input: list[str]) -> str | None:
        score = 0
        for s in input:
            first = s[: len(s) // 2]
            second = s[len(s) // 2 :]
            sf = set(first)
            ss = set(second)
            common = sf.intersection(ss)
            for c in common:
                score += ord(c.lower()) - 96
                if c.upper() == c:
                    score += 26
        return str(score)

    def solveB(self, input: list[str]) -> str | None:
        groups = []
        group = []
        for s in input:
            group.append(s)
            if len(group) == 3:
                groups.append(group)
                group = []
        score = 0
        for g in groups:
            a, b, c = g
            for common in set(a).intersection(set(b)).intersection(set(c)):
                score += ord(common.lower()) - 96
                if common == common.upper():
                    score += 26
        return str(score)
