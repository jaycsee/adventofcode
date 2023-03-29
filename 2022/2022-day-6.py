from collections import Counter

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """mjqjpqmgbljsphdztnvjfqwrcgsmlb""".split("\n")


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "6", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        res = True
        res = self.expect(given, ["7", "19"]) and res
        res = self.expect(["bvwbjplbgvbhsrlpgdmjqwftvncz"], ["5", "23"]) and res
        res = self.expect(["nppdvjthqldpwncqszvftbrmjlhg"], ["6", "23"]) and res
        res = self.expect(["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"], ["10", "29"]) and res
        res = self.expect(["zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"], ["11", "26"]) and res
        return res

    def solveA(self, input: list[str], size=4) -> str | None:
        index = 0
        while True:
            s = input[0][index : index + size]
            buffer = set(s)
            if len(buffer) == size:
                return str(index + size)
            c = Counter(s)
            m = c.most_common()
            index += s.index(m[0][0]) + 1

    def solveB(self, input: list[str]) -> str | None:
        return self.solveA(input, size=14)
