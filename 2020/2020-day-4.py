import re
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2020", "4", timeout=5, sanitized_input=False)

    def test(self) -> bool:
        return self.expect(given, [2, None])

    def solveA(self, input: list[str]) -> str | None:
        ans = 0
        checks = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
        for line in input:
            line = line.strip("\n ")
            if not line: 
                if not checks: ans += 1
                checks = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
            pairs = line.split(" ")
            for p in pairs:
                if not p: continue
                key, value = p.split(":")
                checks.discard(key)
        if not checks: ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        i = 0
        checks = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
        for line in input:
            line = line.strip("\n ")
            if not line: 
                if not checks: 
                    ans += 1
                checks = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
                i += 1
            pairs = line.split(" ")
            for p in pairs:
                if not p: continue
                key, value = p.split(":")
                try: 
                    if key == "byr" and 1920 <= int(value) <= 2002: checks.discard(key)
                    elif key == "iyr" and 2010 <= int(value) <= 2020: checks.discard(key)
                    elif key == "eyr" and 2020 <= int(value) <= 2030: checks.discard(key)
                    elif key == "hgt" and ((re.match("^[0-9]+in$", value) and 59 <= int(value.strip("in")) <= 76) or (re.match("^[0-9]+cm$", value) and 150 <= int(value.strip("cm")) <= 193)): checks.discard(key)
                    elif key == "hcl" and re.match("^#[0-9a-f]{6}$", value): checks.discard(key)
                    elif key == "ecl" and value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]: checks.discard(key)
                    elif key == "pid" and re.match("^[0-9]{9}$", value): checks.discard(key)
                except ValueError as e: pass
        if not checks: ans += 1
        return ans