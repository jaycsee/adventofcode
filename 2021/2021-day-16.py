from puzzle import Puzzle

# Do not run this file. Run it from ../solution.py

from functools import reduce

given1 = """8A004A801A8002F478""".split("\n")
given2 = """620080001611562C8802118E34""".split("\n")
given3 = """C0015000016115A2E0802F182340""".split("\n")
given4 = """A0016C880162017C3686B18A3D4780""".split("\n")

class Solution(Puzzle):
    def __init__(self):
        super().__init__("2021", "16", timeout=5, sanitized_input=True)

    def test(self) -> bool:
        return self.expect(given1, [16, None]) and self.expect(given2, [12, None]) and self.expect(given3, [23, None]) and self.expect(given4, [31, None])

    def parse(self, input: list[str]) -> None:
        input = input[0]
        self.input = []
        for x in input:
            self.input.extend(list(f"{int(x,16):04b}"))
        self.input.reverse()
    
    def readOne(self) -> str:
        if self.input: return self.input.pop()
        return "0"
    
    def read(self, amt: int) -> str:
        return ''.join([self.readOne() for x in range(amt)])
    
    def inputSize(self) -> int:
        return len(self.input)

    def readPacket(self) -> tuple[int, int, int | None, tuple[tuple]]:
        v = int(self.read(3), 2)
        t = int(self.read(3), 2)
        if t == 4:
            n = ""
            while True:
                b = self.read(5)
                n += b[1:]
                if b.startswith("0"): break
            return (v, t, int(n, 2), ())
        else:
            i = self.readOne()
            if i == "0": 
                e = int(self.read(15), 2)
                s = self.inputSize()
                p = []
                while s - self.inputSize() < e: p.append(self.readPacket())
                return (v, t, None, tuple(p))
            else: return (v, t, None, tuple(self.readPacket() for _ in range(int(self.read(11), 2))))


    def solveA(self, input: list[str]) -> str | None:
        self.parse(input)
        ans = 0
        p = [self.readPacket()]
        while p:
            n = []
            for x in p:
                ans += x[0]
                n.extend(x[3])
            p = n
        return ans

    def solveB(self, input: list[str]) -> str | None:
        self.parse(input)
        def process(packet) -> int:
            if packet[1] == 0: return sum([process(x) for x in packet[3]])
            elif packet[1] == 1: return reduce(lambda x,y: x*y, [process(x) for x in packet[3]])
            elif packet[1] == 2: return min([process(x) for x in packet[3]])
            elif packet[1] == 3: return max([process(x) for x in packet[3]])
            elif packet[1] == 4: return packet[2]
            elif packet[1] == 5: return 1 if process(packet[3][0]) > process(packet[3][1]) else 0
            elif packet[1] == 6: return 1 if process(packet[3][0]) < process(packet[3][1]) else 0
            elif packet[1] == 7: return 1 if process(packet[3][0]) == process(packet[3][1]) else 0
        return process(self.readPacket())