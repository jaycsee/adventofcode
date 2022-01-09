from collections import defaultdict
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "7", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [4, 32])

    def processRules(self, input: list[str]):
        self.rules = defaultdict(list)
        self.cache = defaultdict(int)
        for line in input:
            bag, rule = line.strip(".").split(" bags contain ")
            if rule.startswith("no"): continue
            for r in rule.split(", "):
                amt, *color, x = r.split(" ")
                self.rules[bag].append([" ".join(color), int(amt)])

    def recursiveCheck(self, color: str, target: str):
        if color == target: return True
        if color not in self.rules: return False
        for c, v in self.rules[color]:
            if self.recursiveCheck(c, target): return True
        return False

    def getBags(self, color: str):
        if color in self.cache: return self.cache[color]
        if color not in self.rules: return 1
        r = 1
        for c, v in self.rules[color]: 
            r += self.getBags(c) * v
        self.cache[color] = r
        return r

    def solveA(self, input: list[str]) -> str | None:
        self.processRules(input)
        ans = 0
        for r,v in self.rules.items():
            if self.recursiveCheck(r, "shiny gold") and r != "shiny gold": ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        return self.getBags("shiny gold")-1
