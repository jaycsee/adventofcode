from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """30373
25512
65332
33549
35390""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "8", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["21", "8"])

    def solveA(self, input: list[str]) -> str | None:
        grid = [[int(x) for x in y] for y in input]
        visible_mask = [[False for x in y] for y in grid]
        for i in range(len(grid)):
            last = -1
            for j in range(len(grid[i])):
                if grid[i][j] > last:
                    last = grid[i][j]
                    visible_mask[i][j] = True
        for j in range(len(grid[0])):
            last = -1
            for i in range(len(grid)):
                if grid[i][j] > last:
                    last = grid[i][j]
                    visible_mask[i][j] = True
        for i in range(len(grid) - 1, -1, -1):
            last = -1
            for j in range(len(grid[i]) - 1, -1, -1):
                if grid[i][j] > last:
                    last = grid[i][j]
                    visible_mask[i][j] = True
        for j in range(len(grid[0]) - 1, -1, -1):
            last = -1
            for i in range(len(grid) - 1, -1, -1):
                if grid[i][j] > last:
                    last = grid[i][j]
                    visible_mask[i][j] = True
        ans = 0
        for row in visible_mask:
            for col in row:
                if col:
                    ans += 1
        return str(ans)

    def solveB(self, input: list[str]) -> str | None:
        grid = [[int(x) for x in y] for y in input]
        max_score = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                score = 1
                visible = 0
                for v in range(i + 1, len(grid)):
                    visible += 1
                    if grid[i][j] > grid[v][j]:
                        last = grid[v][j]
                    else:
                        break
                score *= visible
                visible = 0
                for v in range(i - 1, -1, -1):
                    visible += 1
                    if grid[i][j] > grid[v][j]:
                        last = grid[v][j]
                    else:
                        break
                score *= visible

                visible = 0
                for v in range(j + 1, len(grid[i])):
                    visible += 1
                    if grid[i][j] > grid[i][v]:
                        last = grid[i][v]
                    else:
                        break
                score *= visible
                visible = 0
                for v in range(j - 1, -1, -1):
                    visible += 1
                    if grid[i][j] > grid[i][v]:
                        last = grid[i][v]
                    else:
                        break
                score *= visible
                max_score = max(max_score, score)
        return str(max_score)
