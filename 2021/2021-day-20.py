from collections import defaultdict
from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py



given = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "20", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [35, 3351])

    def parse(self, input: list[str]) -> None:
        self.table = list(input[0])
        self.empty = "."
        self.images = [] # type: list[list[list[str]]]
        image = []
        for i, line in enumerate(input[1:]):
            image.append(list(line))
        self.images.append(image)
    
    def getPixel(self, image: list[list[str]], x: int, y: int) -> str:
        if not (0 <= x < len(image)) or not (0 <= y < len(image[x])): return self.empty
        return image[x][y]

    def nextImage(self):
        cur = self.images[-1]
        image = []
        image.append([self.empty] * (len(cur[0]) + 2))
        image.extend([[self.empty] + x + [self.empty] for x in cur])
        image.append([self.empty] * (len(cur[0]) + 2))
        new = []
        for i, line in enumerate(image):
            l = []
            for j, val in enumerate(line):
                n = ""
                for xo in range(-1, 2):
                    for yo in range(-1, 2):
                        n += "1" if self.getPixel(image, i+xo, j+yo) == "#" else "0"
                l.append(self.table[int(n, 2)])
            new.append(l)
        self.images.append(new)
        self.empty = self.table[0] if self.empty == "." else self.table[-1]

    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        self.nextImage()
        self.nextImage()
        ans = 0 
        for i, line in enumerate(self.images[-1]): 
            for j, v in enumerate(line):
                if v == "#": ans += 1
        return ans

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        for _ in range(50):
            self.nextImage()
        ans = 0 
        for i, line in enumerate(self.images[-1]): 
            for j, v in enumerate(line):
                if v == "#": ans += 1
        return ans