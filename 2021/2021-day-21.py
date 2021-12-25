from collections import defaultdict
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """Player 1 starting position: 4
Player 2 starting position: 8""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "21", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [739785, 444356092776315])

    def dice1(self):
        while True:
            for i in range(1, 101): 
                self.rolls += 1
                yield i

    def solveA(self, input: list[str]) -> str | None:
        self.rolls = 0
        d = self.dice1()
        p1 = int(input[0].split(": ")[1])
        p2 = int(input[1].split(": ")[1])
        s1 = 0
        s2 = 0
        flag = False
        while s1 < 1000 and s2 < 1000: 
            if not flag:
                p1 += next(d) + next(d) + next(d)
                if p1 > 10: p1 %= 10
                if p1 == 0: p1 = 10
                s1 += p1
            else:
                p2 += next(d) + next(d) + next(d)
                if p2 > 10: p2 %= 10
                if p2 == 0: p2 = 10
                s2 += p2
            flag = not flag
        return min(s1, s2) * self.rolls

    def solveB(self, input: list[str]) -> str | None:
        states = {}
        states[(int(input[0].split(": ")[1]), int(input[1].split(": ")[1]), 0, 0)] = 1
        d = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
        flag = False
        w1 = 0
        w2 = 0
        while states:
            newstates = defaultdict(int)
            for s, a in states.items():
                for v, p in d.items():
                    p1, p2, s1, s2 = s
                    if not flag:
                        p1 += v
                        if p1 > 10: p1 %= 10
                        if p1 == 0: p1 = 10
                        s1 += p1
                        if s1 >= 21: w1 += a * p
                        else: newstates[(p1, p2, s1, s2)] += a * p
                    else: 
                        p2 += v
                        if p2 > 10: p2 %= 10
                        if p2 == 0: p2 = 10
                        s2 += p2
                        if s2 >= 21: w2 += a * p
                        else: newstates[(p1, p2, s1, s2)] += a * p
            flag = not flag
            states = newstates
        return max(w1, w2)
