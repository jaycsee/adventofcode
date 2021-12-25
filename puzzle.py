import abc
import os
import re
import traceback
import requests
import concurrent.futures as futures
import queue
import threading 

class Puzzle:
    """Represents an abstract, extendable class to solve an AOC puzzle"""

    def __init__(self, year: int | str, day: int | str, timeout: int=10, sanitized_input: bool = True) -> None:
        self.year = year
        self.day = day
        self.timeout = timeout
        self.sanitized_input = sanitized_input
        self.cachefile = os.path.join("cache", f"{self.year}day{self.day}.input")
        self.url = f"https://adventofcode.com/{year}/day/{day}"

    def sanitize(self, input: list[str]) -> list[str]:
        """Sanitizes the input if required to by the constructor"""
        if self.sanitized_input: return [x.strip(" \n") for x in input if len(x)]
        return input

    def get_input(self, session: str, sanitized: bool | None = None) -> list[str]:
        """Gets the input of the puzzle associated with session as an list of input lines. By default, lines will be sanitized from whitespaces and empty lines"""
        if sanitized is None: sanitized = self.sanitized_input
        if os.path.exists(self.cachefile):
            with open(self.cachefile, "r") as f:
                c = f.readlines()
        else:
            r = requests.get(self.url + "/input", cookies={"session":session})
            if r.status_code != 200:
                raise ValueError("Couldn't get data")
            c = r.text
            if not os.path.exists(str("cache")): os.mkdir(str("cache"))
            with open(self.cachefile, "w") as f:
                f.write(c)
            c = c.split("\n")
        return self.sanitize(c)

    def get_solution(self, input: list[str], timeout: int | None = None) -> list[str] | None:
        """Attempts to solve part A and B of the puzzle with the given input"""
        input = self.sanitize(input)
        if timeout is None: timeout = self.timeout
        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            futureA = executor.submit(self.solveA, tuple(input))
            resultA = None
            try: resultA = futureA.result(timeout)
            except (futures.TimeoutError, KeyboardInterrupt): 
                print("Part A timed out")
                futureA.cancel()
            futureB = executor.submit(self.solveB, tuple(input))
            resultB = None
            try: resultB = futureB.result(timeout)
            except (futures.TimeoutError, KeyboardInterrupt): 
                print("Part B timed out")
                futureB.cancel()
            executor._threads.clear()
            futures.thread._threads_queues.clear()
            return [resultA, resultB]


    def expect(self, input: str | list[str], expected: list[str]) -> bool:
        """Asserts that the input should result in the answers to part A and B from expected, in that order"""
        while len(expected) < 2: expected.append(None)
        expectedA,expectedB = (None if x is None else str(x) for x in expected)
        ansA,ansB = (None if x is None else str(x) for x in self.get_solution(input))
        passed = True
        if expectedA and ansA != expectedA: 
            passed = False
            print(f"Expected {expectedA} from part A, but instead got {ansA if ansA else 'nothing'}")
        if expectedB and ansB != expectedB: 
            passed = False
            print(f"Expected {expectedB} from part B, but instead got {ansB if ansB else 'nothing'}")
        return passed

    def submit(self, session: str, doit: bool = False, ans: list[str] = None) -> list[str]:
        """Grabs the input for the session and returns the answer to be submitted. Set doit to submit to the server"""
        if ans is None: ans = self.get_solution(self.get_input(session))
        if doit is False: return ans
        cookies = {"session": session}
        ra = None
        rb = None
        if len(ans) > 0 and ans[0] is not None: ra = requests.post(url=self.url + "/answer", cookies=cookies, data={"level": 1, "answer": ans[0]})
        if len(ans) > 1 and ans[1] is not None: rb = requests.post(url=self.url + "/answer", cookies=cookies, data={"level": 2, "answer": ans[1]})
        resA = ""
        if ra is None: resA = "No submission"
        elif ra.status_code != 200: resA = f"Got status {ra.status_code}"
        elif "not the right answer" in ra.text: resA = "Incorrect"
        elif "s the right answer" in ra.text: resA = "Correct"
        elif "already complete it" in ra.text: resA = "N/A"
        elif "answer too recently" in ra.text: 
            [(minutes, seconds)] = re.findall(r"You have (?:(\d+)m )?(\d+)s left to wait", ra.text)
            resA = f"Rate limited. Wait {seconds + minutes * 60} seconds"
        else: resA = "Unknown"
        resB = ""
        if rb is None: resB = "No submission"
        elif rb.status_code != 200: resB = f"Got status {rb.status_code}"
        elif "not the right answer" in rb.text: resB = "Incorrect"
        elif "s the right answer" in rb.text: resB = "Correct"
        elif "already complete it" in rb.text: resB = "N/A"
        elif "answer too recently" in rb.text: 
            [(minutes, seconds)] = re.findall(r"You have (?:(\d+)m )?(\d+)s left to wait", rb.text)
            resB = f"Rate limited. Wait {seconds + minutes * 60} seconds"
        else: resB = "Unknown"
        return (resA, resB)
         
    @abc.abstractmethod
    def test(self) -> bool:
        """Tests whether this solution correctly answers the test cases. Should call expect()"""
        return
    
    @abc.abstractmethod
    def solveA(self, input: list[str]) -> str | None:
        """Solves part A of the puzzle with the given input"""
        return
    
    @abc.abstractmethod
    def solveB(self, input: list[str]) -> str | None:
        """Solves part B of the puzzle with the given input"""
        return