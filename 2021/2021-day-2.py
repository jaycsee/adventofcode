from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "2", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [150, 900])

    def solveA(self, input: list[str]) -> str | None:
        x = 0
        y = 0
        for line in input:
            if line.startswith("forward"): x += int(line.split(" ")[1])
            if line.startswith("up"): y += int(line.split(" ")[1])
            if line.startswith("down"): y -= int(line.split(" ")[1])
        return abs(x * y)

    def solveB(self, input: list[str]) -> str | None:
        x = 0
        y = 0
        aim = 0
        for line in input:
            if line.startswith("forward"): 
                x += int(line.split(" ")[1])
                y += aim * int(line.split(" ")[1])
            if line.startswith("up"): aim += int(line.split(" ")[1])
            if line.startswith("down"): aim -= int(line.split(" ")[1])
        return abs(x * y)