from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

from functools import reduce

given = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "4", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, [4512, 1924])

    def createBoard(self, input: list[str]) -> None:
        self.boards = []
        self.marked = []
        board = []
        mark = []
        for line in input[1:]:
            board.append(line.strip().replace("  ", " ").split(" "))
            mark.append([False] * 5)
            if len(board) == 5: 
                self.boards.append(board)
                self.marked.append(mark)
                board = []
                mark = []

    def markBoard(self, board: int, num: int) -> None:
        for i, line in enumerate(self.boards[board]):
            for j, val in enumerate(line):
                if val == num: self.marked[board][i][j] = True

    def checkWin(self, board: int) -> bool:
        check = lambda x,y: x and y
        for row in self.marked[board]: 
            if reduce(check, row): return True
        for col in range(5):
            if reduce(check, [self.marked[board][row][col] for row in range(5)]): return True
        return False

    def calcScore(self, board: list[str], num: int) -> int:
        ans = 0
        for i, line in enumerate(self.boards[board]):
            for j, val in enumerate(line):
                if not self.marked[board][i][j]: ans += int(val)
        return ans * num

    def solveA(self, input: list[str]) -> str | None:
        nums = input[0].split(",")
        self.createBoard(input)
        for num in nums:
            for b in range(len(self.boards)):
                self.markBoard(b, num)
                if self.checkWin(b): 
                    return self.calcScore(b, int(num))
        return None

    def solveB(self, input: list[str]) -> str | None:
        nums = input[0].split(",")
        self.createBoard(input)
        left = len(self.boards)
        won = [False] * len(self.boards)
        for num in nums:
            for b in range(len(self.boards)):
                if won[b]: continue
                self.markBoard(b, num)
                if self.checkWin(b):
                    left -= 1
                    if left == 0: return self.calcScore(b, int(num))
                    else: won[b] = True
        return None
