from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "8", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [26, 61229])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        for line in input: 
            for c in line.split(" | ")[1].split(" "):
                if len(c) == 2 or len(c) == 4 or len(c) == 3 or len(c) == 7: ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        for line in input:
            decodes, output = line.split(" | ")
            decodes = decodes.split(" ")
            mapping = [None] * 10
            for decode in decodes: 
                s = set(decode)
                if len(decode) == 2: mapping[1] = s
                elif len(decode) == 4: mapping[4] = s
                elif len(decode) == 3: mapping[7] = s
                elif len(decode) == 7: mapping[8] = s
            for decode in decodes:
                s = set(decode)
                if len(decode) == 6: 
                    if not s.issuperset(mapping[1]): mapping[6] = s
                    elif not s.issuperset(mapping[4]): mapping[0] = s
                    else: mapping[9] = s
                elif len(decode) == 5:
                    if s.issuperset(mapping[1]): mapping[3] = s
                    elif len(s.intersection(mapping[4])) == 3: mapping[5] = s
                    else: mapping[2] = s
            i = ""
            for o in output.split(" "):
                for m,s in enumerate(mapping):
                    if len(set(o).symmetric_difference(s)) == 0: i += str(m)
            ans += int(i)
        return ans
