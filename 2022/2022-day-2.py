from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """A Y
B X
C Z""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "2", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["15", "12"])

    def solveA(self, input: list[str]) -> str | None:
        score = 0
        for s in input:
            a, b = s.split(" ")
            if b == "X":  # You choose rock
                score += 1
                if a == "C":
                    score += 6  # They choose scissors
                elif a == "A":
                    score += 3  # They choose rock
            elif b == "Y":  # You choose paper
                score += 2
                if a == "A":
                    score += 6  # They choose rock
                elif a == "B":
                    score += 3  # They choose paper
            elif b == "Z":  # You choose scissors
                score += 3
                if a == "B":
                    score += 6  # They choose paper
                elif a == "C":
                    score += 3  # They choose scissors
        return str(score)

    def solveB(self, input: list[str]) -> str | None:
        score = 0
        for s in input:
            a, b = s.split(" ")
            if b == "X":  # You lose
                if a == "A":
                    score += 3  # They choose rock, you choose scissors
                elif a == "B":
                    score += 1  # They choose paper, you choose rock
                elif a == "C":
                    score += 2  # They choose scissors, you choose paper
            elif b == "Y":  # You draw
                score += 3
                if a == "A":
                    score += 1  # They choose rock
                elif a == "B":
                    score += 2  # They choose paper
                elif a == "C":
                    score += 3  # They choose scissors
            elif b == "Z":  # You win
                score += 6
                if a == "A":
                    score += 2  # They choose rock, you choose paper
                elif a == "B":
                    score += 3  # They choose paper, you choose scissors
                elif a == "C":
                    score += 1  # They choose scissors, you choose rock
        return str(score)
