from __future__ import annotations
from typing import Iterable
from puzzle import Puzzle
from copy import deepcopy

# Do not run this file. Run it from ../solution.py

import sys
sys.setrecursionlimit(10**6)

class Node:
    def __str__(self) -> str:
        if self.val is not None: return str(self.val)
        return f"[{self.left},{self.right}]"

    def __init__(self, parent: Node | None, leftside: bool, depth: int):
        self.parent = parent
        self.leftside = leftside
        self.depth = depth
        self.val = None # type: int
        self.left = None # type: Node
        self.right = None # type: Node
    
    def explode(self):
        self.parent.handleExplode(self.leftside)
    
    def handleExplode(self, leftside: bool):
        if leftside:
            lv = self.left.left.val
            rv = self.left.right.val
            self.parent.addLeft(self.leftside, lv)
            self.addRight(True, rv)
            self.left = Node(self, True, self.depth + 1)
            self.left.val = 0
        else:
            lv = self.right.left.val
            rv = self.right.right.val
            self.addLeft(False, lv)
            self.parent.addRight(self.leftside, rv)
            self.right = Node(self, False, self.depth + 1)
            self.right.val = 0
    
    def addLeft(self, fromleft: bool, v: int):
        if not fromleft: 
            n = self.left
            while n.right: 
                n = n.right
            n.val += v
        elif self.parent: self.parent.addLeft(self.leftside, v)
        
    def addRight(self, fromleft: bool, v: int):
        if fromleft: 
            n = self.right
            while n.left: 
                n = n.left
            n.val += v
        elif self.parent: self.parent.addRight(self.leftside, v)

    def checkExplode(self) -> bool:
        if self.depth >= 4 and self.left and self.left.val is not None and self.right and self.right.val is not None: 
            self.explode()
            return True
        if self.left:
            r = False
            r = self.left.checkExplode() or r
            r = self.right.checkExplode() or r
            return r
        return False

    def checkSplit(self) -> bool:
        if self.val is not None and self.val > 9: 
            self.left = Node(self, True, self.depth + 1)
            self.left.val = self.val // 2
            self.right = Node(self, False, self.depth + 1)
            self.right.val = self.val - self.left.val
            self.val = None
            self.checkExplode()
            return True
        if self.left: 
            if self.left.checkSplit(): return True
            if self.right.checkSplit(): return True
        return False
    
    def addDepth(self) -> None:
        self.depth += 1
        if self.left: 
            self.left.addDepth()
            self.right.addDepth()

    def magnitude(self) -> int:
        if self.val is not None: return self.val
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    @staticmethod
    def gen(s, parent: Node | None, leftside: bool, depth: int) -> Node:
        n = Node(parent, leftside, depth)
        v = next(s)
        if v.isnumeric(): 
            n.val = int(v)
            return n
        n.left = Node.gen(s, n, True, depth+1)
        next(s)
        n.right = Node.gen(s, n, False, depth+1)
        next(s)
        return n

    @staticmethod
    def add(left: Node, right: Node) -> Node:
        n = Node(None, False, 0)
        left = deepcopy(left)
        right = deepcopy(right)
        left.addDepth()
        right.addDepth()
        left.parent = n
        left.leftside = True
        right.parent = n
        right.leftside = False
        n.left = left
        n.right = right
        return n

test = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".split("\n")

# test = """[[[[4,3],4],4],[7,[[8,4],9]]]
# [1,1]""".split("\n")

given = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "18", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(test, [3488, None]) and self.expect(given, [4140, 3993])

    def solveA(self, input: list[str]) -> str | None:
        nodes = []
        for line in input:
            nodes.append(Node.gen(iter(line), None, False, 0))
        n = nodes[0]
        for node in nodes[1:]:
            n = Node.add(n, node)
            while True:
                if n.checkExplode(): continue
                if n.checkSplit(): continue
                break
        return n.magnitude()

    def solveB(self, input: list[str]) -> str | None:
        ans = 0
        nodes = []
        for line in input:
            nodes.append(Node.gen(iter(line), None, False, 0))
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j: continue
                n = Node.add(nodes[i], nodes[j])
                while True:
                    if n.checkExplode(): continue
                    if n.checkSplit(): continue
                    break
                ans = max(ans, n.magnitude())
        return ans
