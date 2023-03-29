from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "1", timeout=5, sanitized_input=False)

    def test(self) -> bool:
        return self.expect(given, ["24000", "45000"])

    def get_sums(self, input: list[str]) -> list[int]:
        elves = []
        elf = []
        for s in input:
            if s.strip() == "":
                elves.append(elf)
                elf = []
            else:
                elf.append(int(s))
        if elf:
            elves.append(elf)
        sums = [sum(x) for x in elves]
        return sums

    def solveA(self, input: list[str]) -> str | None:
        sums = self.get_sums(input)
        return str(max(sums))

    def solveB(self, input: list[str]) -> str | None:
        sums = self.get_sums(input)
        sums.sort()
        return sum(sums[-3:])
