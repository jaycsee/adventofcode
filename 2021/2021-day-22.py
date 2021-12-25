from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "22", timeout=20, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [590784, None])

    def solveA(self, input: list[str]) -> str | None:
        m = []
        for line in reversed(input):
            x, y, z = line.strip("onf ").split(",")
            xs, xe = x.strip("x=").split("..")
            ys, ye = y.strip("y=").split("..")
            zs, ze = z.strip("z=").split("..")
            v = line.startswith("on")
            m.append(tuple(int(x) for x in (xs, xe, ys, ye, zs, ze, v)))
            if abs(m[-1][0]) > 100: m.pop()
        def find(x: int, y: int, z: int) -> bool:
            for xs, xe, ys, ye, zs, ze, v in m:
                if xs <= int(x) <= xe and ys <= int(y) <= ye and zs <= int(z) <= ze: return v
            return False
        ans = 0
        for x in range(-50, 51):
            for y in range(-50, 51):
                for z in range(-50, 51):
                    if find(x, y, z): ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        return None
