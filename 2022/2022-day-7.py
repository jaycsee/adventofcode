from __future__ import annotations

from dataclasses import dataclass, field

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split(
    "\n"
)


@dataclass
class Dir:
    name: str
    parent: Dir | None = None
    files: list[int] = field(default_factory=list)
    children: dict[str, Dir] = field(default_factory=dict)

    def size(self) -> tuple[int, int]:
        # ans, totalsize
        ans = 0
        size = sum(self.files)
        for x in self.children.values():
            subans, subsize = x.size()
            ans += subans
            size += subsize
        if size <= 100000:
            ans += size
        return ans, size

    def dirSizes(self) -> tuple[list[int], int]:
        ans = []
        size = sum(self.files)
        for x in self.children.values():
            subsizes, subsize = x.dirSizes()
            ans.extend(subsizes)
            size += subsize
        ans.append(size)
        return ans, size


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "7", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["95437", "24933642"])

    def solveA(self, input: list[str]) -> str | None:
        tree = Dir("root")
        root = tree
        i = 0
        while i < len(input):
            command = input[i]
            d, command, *cdir = command.split(" ")
            if d != "$":
                i += 1
                continue
            if command == "cd":
                if cdir[0] == "..":
                    assert tree.parent
                    tree = tree.parent
                    i += 1
                    continue
                elif cdir[0] == "/":
                    tree = root
                    i += 1
                    continue
                if cdir[0] not in tree.children:
                    tree.children[cdir[0]] = Dir(cdir[0], tree)
                tree = tree.children[cdir[0]]
                i += 1
            elif command == "ls":
                i += 1
                files: list[int] = []
                while i < len(input) and not input[i].startswith("$"):
                    size, name = input[i].split(" ")
                    if size.isnumeric():
                        files.append(int(size))
                    i += 1
                tree.files = files
        self.root = root
        return str(root.size()[0])

    def solveB(self, input: list[str]) -> str | None:
        self.solveA(input)
        ss, size = self.root.dirSizes()
        required = size - (70000000 - 30000000)
        ss.sort()
        for x in ss:
            if x >= required:
                return str(x)
        raise ValueError()
