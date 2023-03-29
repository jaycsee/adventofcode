from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "5", timeout=5, sanitized_input=False)

    def test(self) -> bool:
        return self.expect(given, ["CMZ", "MCD"])

    def solveA(self, input: list[str], multi=False) -> str | None:
        rows = []
        for s in input:
            if s.strip() == "":
                break
            rows.append(s[1::4])
        rows = rows[:-1]
        stacks = []
        for i in range(max([len(x) for x in rows])):
            stacks.append([rows[-j - 1][i] for j in range(len(rows)) if rows[-j - 1][i].strip()])
        found = False
        for s in input:
            if s.strip() == "":
                found = True
                continue
            if not found:
                continue
            _, amt, _, fr, _, to, *_ = s.split(" ")
            amt = int(amt)
            fr = int(fr) - 1
            to = int(to) - 1
            move = stacks[fr][-amt:]
            stacks[fr] = stacks[fr][:-amt]
            if not multi:
                move.reverse()
            stacks[to].extend(move)
        return "".join([x[-1] for x in stacks])

    def solveB(self, input: list[str]) -> str | None:
        return self.solveA(input, True)
