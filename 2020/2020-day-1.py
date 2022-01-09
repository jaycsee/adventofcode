from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """1721
979
366
299
675
1456""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "1", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [514579, 241861950])

    def solveA(self, input: list[str]) -> str | None:
        numbers = set()
        for line in input:
            x = int(line)
            if 2020-x in numbers: return x*(2020-x)
            numbers.add(x)
        return None

    def solveB(self, input: list[str]) -> str | None:
        numbers = set()
        for line in input:
            numbers.add(int(line))
        for i,x in enumerate((l := list(numbers))): 
            for j,y in enumerate(l):
                if i == j: continue
                if (n := 2020-x-y) in numbers and n != x and n != y: return n*x*y
        return None
