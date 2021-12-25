from requests.sessions import default_headers
from puzzle import Puzzle
from collections import defaultdict

# Do not run this file. Run it from ../solution.py



given = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "14", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [1588, 2188189693529])

    def parse(self, input: list[str]) -> None:
        self.state = defaultdict(int)
        self.fl = [input[0][0], input[0][-1]]
        for i in range(1, len(input[0])): self.state[input[0][i-1] + input[0][i]] += 1
        self.table = {}
        for line in input[1:]:
            m, a = line.split(" -> ")
            k1, k2 = list(m)
            if k1 not in self.table:
                self.table[k1] = {}
            self.table[k1][k2] = a
    
    def step(self) -> None:
        new = defaultdict(int)
        for k,v in self.state.items():
            k1, k2 = list(k)
            l = self.table[k1][k2]
            new[k1 + l] += v
            new[l + k2] += v
        self.state = new

    def count(self) -> list[int]:
        r = defaultdict(int)
        for k,v in self.state.items():
            k1, k2 = list(k)
            r[k1] += v
            r[k2] += v
        for k in self.fl: r[k] += 1
        return [x // 2 for x in list(r.values())]

    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        for _ in range(10): self.step()
        c = sorted(self.count())
        return c[-1] - c[0]

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        for _ in range(40): self.step()
        c = sorted(self.count())
        return c[-1] - c[0]