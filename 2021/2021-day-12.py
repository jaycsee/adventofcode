from collections import defaultdict
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

given1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n")

given2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".split("\n")

given3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "12", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given1, [10, 36]) and self.expect(given2, [19, 103]) and self.expect(given3, [226, 3509])

    def parse(self, input: list[str]) -> None:
        self.smalls = set()
        self.paths = defaultdict(set)
        for line in input:
            src, dest = line.split("-")
            self.paths[src].add(dest)
            self.paths[dest].add(src)
            if src.islower(): self.smalls.add(src)
            if dest.islower(): self.smalls.add(dest)

    def search(self, node, smallsleft: set, twiced: bool):
        if node == "end":
            return 1
        if node == "start":
            return 0
        if node.islower() and node not in smallsleft:
            if twiced:
                return 0
            twiced = True
        smallsleft.discard(node)
        ret = sum([self.search(x, smallsleft.copy(), twiced) for x in sorted(self.paths[node] if node in self.paths else set())])
        return ret

    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        ans = 0
        for x in self.paths["start"]:
            smallsleft = self.smalls.copy()
            ans += self.search(x, smallsleft, True)
        return ans
        

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        ans = 0
        for x in self.paths["start"]:
            smallsleft = self.smalls.copy()
            ans += self.search(x, smallsleft, False)
        return ans
