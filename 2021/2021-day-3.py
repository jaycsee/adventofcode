from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "3", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [198, 230])

    def solveA(self, input: list[str]) -> str | None:
        zeros = [0] * len(input[0])
        ones = [0] * len(input[0])
        for line in input:
            for i,x in enumerate(line):
                if x == "0": zeros[i] += 1
                else: ones[i] += 1
        gamma = ''.join(["0" if zeros[i] > ones[i] else "1" for i in range(len(input[0]))])
        epsilon = ''.join(["0" if zeros[i] < ones[i] else "1" for i in range(len(input[0]))])
        return int(gamma, 2) * int(epsilon, 2)

    def solveB(self, input: list[str]) -> str | None:
        oxy = set(input)
        co2 = set(input)
        i = 0
        drop = set()
        while len(oxy) > 1:
            zeros = 0
            ones = 0
            for x in oxy:
                if x[i] == "0": zeros += 1
                else: ones += 1
            for x in oxy:
                if (zeros > ones and x[i] == "1") or (ones >= zeros and x[i] == "0"): drop.add(x)
            i += 1
            oxy -= drop 
        i = 0
        drop = set()
        while len(co2) > 1:
            zeros = 0
            ones = 0
            for x in co2:
                if x[i] == "0": zeros += 1
                else: ones += 1
            for x in co2:
                if (zeros > ones and x[i] != "1") or (ones >= zeros and x[i] != "0"): drop.add(x)
            i += 1
            co2 -= drop 
        return int(oxy.pop(), 2) * int(co2.pop(), 2)