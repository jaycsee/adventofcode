from __future__ import annotations

from collections import Counter, deque
from typing import Callable

from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py


given = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".split(
    "\n"
)


class Item:
    worry: int
    pf: Counter[int]
    primes = None
    cache = {}

    def __init__(self, worry: int, pf: Counter[int] | None = None) -> None:
        self.worry = worry
        if pf is not None:
            self.pf = pf
            return
        self.pf = Counter()
        if Item.primes is None:
            print("Computing primes")
            primes = [2, 3, 5]
            for i in range(7, 100):
                is_prime = True
                for p in primes:
                    if i % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(i)
            Item.primes = primes

        if self.worry in Item.cache:
            self.pf = Item.cache[self.worry].copy()
        else:
            for p in Item.primes:
                x = worry
                f = 0
                while x > 1:
                    if x % p == 0:
                        x = x // p
                        f += 1
                        continue
                    break
                if f != 0:
                    self.pf[p] = f
            Item.cache[self.worry] = self.pf
        new_worry = 1
        for k, v in self.pf.items():
            if k >= 2:
                new_worry *= k**v
        self.worry = new_worry

    def __add__(self, other: Item | int) -> Item:
        if isinstance(other, int):
            other = Item(other)
        return Item(self.worry + other.worry)

    def __mul__(self, other: Item | int) -> Item:
        if isinstance(other, int):
            other = Item(other)
        result = Counter()
        for k, v in self.pf.items():
            result[k] += v
        for k, v in other.pf.items():
            result[k] += v
        return Item(self.worry * other.worry, result)

    def __floordiv__(self, other: Item | int) -> Item:
        if isinstance(other, int):
            other = Item(other)
        f = self.pf.get(3)
        if not f or not f > 0:
            return Item(self.worry // other.worry)
        result = self.pf.copy()
        result[3] -= 1
        return Item(self.worry // other.worry, result)

    def divisible_by(self, other: Item | int) -> bool:
        if isinstance(other, int):
            other = Item(other)
        for k, v in other.pf.items():
            vs = self.pf.get(k)
            if not vs or v > vs:
                return False
        return True


class Monkey:
    def __init__(self, items: list[Item], monkeys: list[Monkey], op: Callable[[Item], Item], compare: Callable[[Item], bool], if_true: int, if_false: int) -> None:
        self.items = deque(items)
        self.monkeys = monkeys
        self.compare = compare
        self.op = op
        self.if_true = if_true
        self.if_false = if_false

        self.inspected = 0

    def add(self, item: Item):
        self.items.append(item)

    def inspect(self):
        while self.items:
            old = self.items.popleft()
            item = self.op(old)
            self.inspected += 1
            if self.compare(item):
                self.monkeys[self.if_true].add(item)
            else:
                self.monkeys[self.if_false].add(item)


class Solution(Puzzle):
    def __init__(self):
        super().__init__("2022", "11", timeout=30, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given, ["10605", "2713310158"])

    def parse(self, input: list[str], div3: bool = True) -> list[Monkey]:
        monkeys: list[Monkey] = []
        gen = iter(input)
        while True:
            s = next(gen, None)
            if not s:
                break
            assert s.startswith("Monkey")
            s = next(gen)
            assert s.startswith("Starting items: ")
            items = [Item(x) for x in eval(f"[{s[16:]}]")]
            s = next(gen)
            assert s.startswith("Operation: ")
            op = eval(f"lambda old: ({s[17:]}) {'// 3' if div3 else ''}")
            s = next(gen)
            assert s.startswith("Test: divisible by ")
            compare = eval(f"lambda old: old.divisible_by({s[19:]})")
            s = next(gen)
            assert s.startswith("If true: throw to monkey ")
            if_true = int(s[25:])
            s = next(gen)
            assert s.startswith("If false: throw to monkey ")
            if_false = int(s[26:])
            monkeys.append(Monkey(items, monkeys, op, compare, if_true, if_false))
        return monkeys

    def solveA(self, input: list[str]) -> str | None:
        return
        monkeys = self.parse(input)
        for i in range(20):
            # print(f"Round {i}")
            for i, m in enumerate(monkeys):
                m.inspect()
        inspects = []
        for m in monkeys:
            inspects.append(m.inspected)
        inspects.sort()
        print(inspects)
        return inspects[-1] * inspects[-2]

    def solveB(self, input: list[str]) -> str | None:
        return
        monkeys = self.parse(input, False)
        for i in range(10000):
            print(f"Round {i}")
            for m in monkeys:
                m.inspect()
        inspects = []
        for m in monkeys:
            inspects.append(m.inspected)
        inspects.sort()
        return inspects[-1] * inspects[-2]
