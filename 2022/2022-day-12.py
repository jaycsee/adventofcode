from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "12", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["31", "29"])

    def solveA(self, input: list[str]) -> str | None:
        grid: list[list[int]] = []
        visited: set[tuple[int, int]] = set()
        search: list[tuple[int, int]] = []
        trow = 0
        tcol = 0
        for i, line in enumerate(input):
            g = []
            for j, c in enumerate(line):
                h = ord(c) - 96
                if c == "S":
                    search.append((i, j))
                    visited.add((i, j))
                    h = 1
                elif c == "E":
                    trow = i
                    tcol = j
                    h = 26
                g.append(h)
            grid.append(g)
        steps = 0
        while True:
            steps += 1
            new_search = []
            for s in search:
                candidates = [
                    (s[0] + 1, s[1]),
                    (s[0], s[1] + 1),
                    (s[0] - 1, s[1]),
                    (s[0], s[1] - 1),
                ]
                for c in candidates:
                    if 0 <= c[0] < len(grid) and 0 <= c[1] < len(grid[0]) and c not in visited and grid[c[0]][c[1]] - 1 <= grid[s[0]][s[1]]:
                        if c == (trow, tcol):
                            return str(steps)
                        visited.add(c)
                        new_search.append(c)
            search = new_search
            if not new_search:
                return None

    def solveB(self, input: list[str]) -> str | None:
        grid: list[list[int]] = []
        visited: set[tuple[int, int]] = set()
        search: list[tuple[int, int]] = []
        for i, line in enumerate(input):
            g = []
            for j, c in enumerate(line):
                h = ord(c) - 96
                if c == "E":
                    search.append((i, j))
                    visited.add((i, j))
                    h = 26
                elif c == "S":
                    h = 1
                g.append(h)
            grid.append(g)
        steps = 0
        while True:
            steps += 1
            new_search = []
            for s in search:
                candidates = [
                    (s[0] + 1, s[1]),
                    (s[0], s[1] + 1),
                    (s[0] - 1, s[1]),
                    (s[0], s[1] - 1),
                ]
                for c in candidates:
                    if 0 <= c[0] < len(grid) and 0 <= c[1] < len(grid[0]) and c not in visited and grid[c[0]][c[1]] >= grid[s[0]][s[1]] - 1:
                        if grid[c[0]][c[1]] == 1:
                            return str(steps)
                        visited.add(c)
                        new_search.append(c)
            search = new_search
            if not new_search:
                return None
