from typing import Callable

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split(
    "\n"
)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "9", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["13", "1"]) and self.expect(["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"], [None, "36"])

    def solveA(self, input: list[str]) -> str | None:
        head = (0, 0)
        tail = (0, 0)
        visited = set([(0, 0)])

        dist = lambda x, y: max(abs(x[0] - y[0]), abs(x[1] - y[1]))

        for s in input:
            direction, amt = s.split(" ")
            if direction == "R":
                f = lambda x, a: (x[0] + a, x[1])
            elif direction == "L":
                f = lambda x, a: (x[0] - a, x[1])
            elif direction == "U":
                f = lambda x, a: (x[0], x[1] + a)
            elif direction == "D":
                f = lambda x, a: (x[0], x[1] - a)
            else:
                assert False
            for i in range(int(amt)):
                newhead = f(head, 1)
                if dist(head, tail) == 1 and dist(newhead, tail) == 2:
                    tail = head
                elif dist(newhead, tail) > 1:
                    tail = f(tail, 1)
                head = newhead
                visited.add(tail)
        return str(len(visited))

    def printPos(self, pos, min: int, max: int):
        for i in range(min, max):
            for j in range(min, max):
                print(x if (x := ((j, -i) in pos and pos.index((j, -i)))) is not False else ".", end="")
            print()

    def solveB(self, input: list[str]) -> str | None:
        pos: list[tuple[int, int]] = [(0, 0) for i in range(10)]
        visited: set[tuple[int, int]] = set([(0, 0)])
        Position = tuple[int, int]
        touching: Callable[[Position, Position], bool] = lambda x, y: max(abs(x[0] - y[0]), abs(x[1] - y[1])) <= 1
        dist: Callable[[Position, Position], int] = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])

        for line, s in enumerate(input):
            direction, amt = s.split(" ")
            amt = int(amt)
            f: Callable[[Position], Position]
            if direction == "R":
                f = lambda x: (x[0] + 1, x[1])
            elif direction == "L":
                f = lambda x: (x[0] - 1, x[1])
            elif direction == "U":
                f = lambda x: (x[0], x[1] + 1)
            elif direction == "D":
                f = lambda x: (x[0], x[1] - 1)
            else:
                assert False
            for step in range(amt):
                newpos = pos.copy()
                newpos[0] = f(pos[0])
                for i in range(len(pos) - 1):
                    i += 1
                    if not touching(newpos[i], newpos[i - 1]):
                        # if distance is 2, take their old position, if distance is 3, step diagonally
                        if dist(newpos[i], newpos[i - 1]) > 2:
                            newpos[i] = min(
                                [
                                    (newpos[i][0] + 1, newpos[i][1] + 1),
                                    (newpos[i][0] + 1, newpos[i][1] - 1),
                                    (newpos[i][0] - 1, newpos[i][1] + 1),
                                    (newpos[i][0] - 1, newpos[i][1] - 1),
                                ],
                                key=lambda x: dist(x, newpos[i - 1]),
                            )
                        elif dist(newpos[i], newpos[i - 1]) == 2:
                            newpos[i] = min(
                                [
                                    (newpos[i][0] + 1, newpos[i][1]),
                                    (newpos[i][0], newpos[i][1] - 1),
                                    (newpos[i][0], newpos[i][1] + 1),
                                    (newpos[i][0] - 1, newpos[i][1]),
                                ],
                                key=lambda x: dist(x, newpos[i - 1]),
                            )
                        else:
                            assert False, (newpos[i], newpos[i - 1])
                    else:
                        break
                    visited.add(newpos[-1])
                pos = newpos
                visited.add(newpos[-1])
        return str(len(visited))
