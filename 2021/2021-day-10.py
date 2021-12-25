from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "10", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [26397, 288957])

    def solveA(self, input: list[str]) -> str | None:
        table = { ")": 3, "]": 57, "}": 1197, ">": 25137 }
        ans = 0
        for line in input:
            stack = []
            for i in line:
                if i == "(": stack.append(")")
                elif i == "[": stack.append("]")
                elif i == "{": stack.append("}")
                elif i == "<": stack.append(">")
                elif stack.pop() != i: 
                    ans += table[i]
                    break
        return ans

    def solveB(self, input: list[str]) -> str | None:
        table = { ")": 1, "]": 2, "}": 3, ">": 4 }
        scores = []
        for line in input:
            stack = []
            valid = True
            score = 0
            for i in line:
                if i == "(": stack.append(")")
                elif i == "[": stack.append("]")
                elif i == "{": stack.append("}")
                elif i == "<": stack.append(">")
                elif stack.pop() != i: 
                    valid = False
                    break
            if not valid: continue
            while stack:
                i = stack.pop()
                score = score * 5 + table[i]
            scores.append(score)
        scores.sort()
        return scores[len(scores)//2]