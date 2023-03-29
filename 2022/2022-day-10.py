from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "10", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["13140", None])

    def solveA(self, input: list[str]) -> str | None:
        x = 1
        cycle = 0
        ans = 0

        def tick():
            nonlocal cycle, ans
            cycle += 1
            if cycle % 40 == 20:
                ans += x * cycle

        for s in input:
            instruction, *rest = s.split(" ")
            if instruction == "noop":
                tick()
            elif instruction == "addx":
                tick()
                tick()
                x += int(rest[0])
        return str(ans)

    def solveB(self, input: list[str]) -> str | None:
        x = 1
        cycle = 0

        def tick():
            nonlocal cycle
            cycle += 1
            if abs(((cycle - 1) % 40) - x) <= 1:
                print("#", end="")
            else:
                print(".", end="")
            if cycle % 40 == 0:
                print("")

        for s in input:
            instruction, *rest = s.split(" ")
            if instruction == "noop":
                tick()
            elif instruction == "addx":
                tick()
                tick()
                x += int(rest[0])
        return None
