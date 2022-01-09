from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "5", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [820, None])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        for line in input:
            rows = 0
            rowe = 128
            cols = 0
            cole = 8
            for c in line:
                if c == "F": rowe -= (rowe - rows)//2
                elif c == "B": rows += (rowe - rows)//2
                elif c == "R": cols += (cole - cols)//2
                elif c == "L": cole -= (cole - cols)//2
            i = rows*8+cols
            ans = max(i, ans)
        return ans

    def solveB(self, input: list[str]) -> str | None:
        ids = set()
        for line in input:
            rows = 0
            rowe = 128
            cols = 0
            cole = 8
            for c in line:
                if c == "F": rowe -= (rowe - rows)//2
                elif c == "B": rows += (rowe - rows)//2
                elif c == "R": cols += (cole - cols)//2
                elif c == "L": cole -= (cole - cols)//2
            ids.add(rows*8+cols)
        for i in ids:
            if i-1 not in ids and i-2 in ids: return i-1
            elif i+1 not in ids and i+2 in ids: return i+1

