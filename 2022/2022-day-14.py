from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".split(
    "\n"
)


@dataclass
class FreeSpace:
    next_free: int | None

    def __repr__(self) -> str:
        if self.next_free is None:
            return "<EmptySpace>"
        return f"FreeSpace({self.next_free})"


class Column:
    def __init__(self, col: int | None = None, occupied: set[tuple[int, int]] | None = None) -> None:
        empty = FreeSpace(None)
        self.free: defaultdict[int, FreeSpace | None] = defaultdict(lambda: empty)
        if occupied:
            occ = set(x[1] for x in (filter(lambda x: x[0] == col, list(occupied))))
            cur = max(occ)
            fs: FreeSpace | None = None
            for x in range(cur, -1, -1):
                if x in occ:
                    self.free[x] = None
                    fs = None
                    continue
                if fs is None:
                    fs = FreeSpace(x)
                self.free[x] = fs

    def get_freespace(self, row: int) -> FreeSpace | None:
        assert row >= 0
        return self.free[row]

    def settle(self, row: int) -> None:
        assert row >= 0
        free_space = self.free[row]
        if free_space is None:
            raise ValueError("Attempted to settle an occupied position")
        self.free[row] = None
        above_space = self.free[row - 1]
        if row == 0 or above_space is None:
            return
        above_space.next_free = row - 1

    def __repr__(self) -> str:
        ret: list[str] = []
        values = []
        for value in self.free.values():
            if value not in values:
                values.append(value)
        for value in values:
            if value is None:
                continue
            low = None
            high = None
            for key, v in self.free.items():
                if v is not value:
                    continue
                if low is None or high is None:
                    low = key
                    high = key
                low = min(low, key)
                high = max(high, key)
            ret.append(f"{low}-{high}: {value}")
        occupied = []
        for k, v in self.free.items():
            if v is None:
                occupied.append(k)
        occupied.sort()
        if occupied:
            occupied = f"{occupied=}, "
        else:
            occupied = ""
        return f"Column({occupied}{', '.join(ret)})"


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "14", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["29", None])

    def solveA(self, input: list[str]) -> str | None:
        occupied: set[tuple[int, int]] = set()
        process: set[int] = set()
        for s in input:
            start, *points = s.split(" -> ")
            x, y = start.split(",")
            x = int(x)
            y = int(y)
            for p in points:
                tx, ty = p.split(",")
                tx = int(tx)
                ty = int(ty)
                while x != tx or y != ty:
                    occupied.add((x, y))
                    process.add(x)
                    if x != tx:
                        x += (tx - x) // abs(tx - x)
                    if y != ty:
                        y += (ty - y) // abs(ty - y)
        cols = defaultdict(Column)
        for c in process:
            cols[c] = Column(c, occupied)

        try:
            for ans in range(5000):
                col = 500
                row = 0
                done = True
                while True:
                    free_space = cols[col].get_freespace(row)
                    if free_space is None:
                        raise ValueError("Found invalid free space")
                    next_free = free_space.next_free
                    if next_free is None:
                        if done:
                            return str(ans + 1)
                        break
                    if cols[col - 1].get_freespace(next_free + 1) is not None:
                        col = col - 1
                        row = next_free + 1
                        continue
                    elif cols[col + 1].get_freespace(next_free + 1) is not None:
                        col = col + 1
                        row = next_free + 1
                        continue
                    else:
                        cols[col].settle(next_free)
                        break

            raise ValueError("Could not find an answer in the limit")
        finally:
            # print(cols)
            for y in range(0, 200):
                for x in range(440, 560):
                    if (x, y) in occupied:
                        print("#", end="")
                    elif cols[x].get_freespace(y) is None:
                        print("o", end="")
                    else:
                        print(".", end="")
                print()

    def solveB(self, input: list[str]) -> str | None:
        return None
