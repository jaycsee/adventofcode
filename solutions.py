import os
import subprocess
import sys
import traceback
from collections import defaultdict

sys.setrecursionlimit(10**6)

from puzzle import Puzzle

login = ""
try:
    with open("login.txt", "r") as f:
        login = f.readline().strip()
except:
    pass


def main():
    global login
    if "login" not in globals() or login is None:
        print("You are not logged in. Use `login` to log in")
    previous = []
    confirm = None
    year = None
    day = None
    lastins = []
    redo = False
    submitans = None
    badans = defaultdict(set)
    while True:
        command, *args = [x.strip() for x in input(">>> ").strip().split(" ")]
        command = command.lower()
        args = [x for x in args if x]
        if len(command) == 0:
            command = previous
            redo = True
        else:
            redo = False
            lastins = []
        if command == "confirm":
            if confirm is False:
                confirm = True
                command = previous
            else:
                print("Nothing to confirm")
                previous = command
                continue
        if len(command) == 0:
            continue
        elif command == "select":
            if len(args) == 0:
                print("Usage: select <year> <day>")
                continue
            else:
                try:
                    year = int(args[0])
                    day = int(args[1])
                    if year < 2000:
                        year += 2000
                except ValueError:
                    traceback.print_exc()
        elif command == "login":
            login = " ".join(args)
        elif command == "create" or command == "delete" or command == "reset" or command == "input" or command == "expect" or command == "test" or command == "submit":
            if confirm is False:
                confirm = None
            if year is None:
                print("First, select a year and date with `select`")
            else:
                file = os.path.join(str(year), f"{year}-day-{day}.py")
                if command == "create":
                    if os.path.exists(file):
                        print("File already exists")
                    else:
                        if not os.path.exists(str(year)):
                            os.mkdir(str(year))
                        with open("template.py", "r") as template, open(file, "w") as new:
                            new.write(template.read().replace("{{{year}}}", str(year)).replace("{{{day}}}", str(day)))
                        subprocess.run(f"code {file}", shell=True)
                        print("File created")
                elif command == "delete":
                    if not os.path.exists(file):
                        print("File doesn't exist")
                    else:
                        if confirm:
                            os.remove(file)
                            print("File removed")
                            confirm = None
                        else:
                            confirm = False
                            print("Use `confirm` to confirm")
                elif command == "reset":
                    if confirm:
                        os.remove(file)
                        with open("template.py", "r") as template, open(file, "w") as new:
                            new.write(template.read().replace("{{{year}}}", str(year)).replace("{{{day}}}", str(day)))
                        print("File reset")
                        confirm = None
                    else:
                        confirm = False
                        print("Use `confirm` to confirm")
                elif not os.path.exists(file):
                    print("File doesn't exist")
                elif command == "input" or command == "expect" or command == "test" or command == "submit":
                    try:
                        with open(file, "r") as f:
                            exec(f.read(), globals(), globals())
                        if "Solution" not in globals():
                            print("No class `Solution` was found in the file")
                        else:
                            sol = globals()["Solution"]()  # type: Puzzle
                            if command == "test":
                                print("Test passed" if sol.test() else "Test failed")
                            elif command == "expect" and len(args) == 0:
                                print("Usage: expect <value A> [value B]")
                            elif command == "submit" and login is None:
                                print("You are not logged in. Use `login` to log in")
                            elif command == "submit":
                                if confirm:
                                    print("Submitting...")
                                    if not submitans:
                                        print("Attempted to submit an empty answer")
                                        continue
                                    r = sol.submit(login, True, submitans)
                                    print(f"Results: [A] {r[0]}, [B] {r[1]}")
                                    if r[0] == "Incorrect":
                                        badans[f"{year}-day-{day}a.py"].add(submitans[0])
                                    if r[1] == "Incorrect":
                                        badans[f"{year}-day-{day}b.py"].add(submitans[1])
                                    confirm = None
                                else:
                                    submitans = sol.submit(login, False)
                                    print(f"Answers to be submitted: [A] {submitans[0]}, [B] {submitans[1]}")
                                    if submitans[0] in badans[f"{year}-day-{day}a.py"]:
                                        print(f"Warning: {submitans[0]} was already submitted as an incorrect answer for part A")
                                    if submitans[1] in badans[f"{year}-day-{day}b.py"]:
                                        print(f"Warning: {submitans[1]} was already submitted as an incorrect answer for part B")
                                    confirm = False
                                    print("Use `confirm` to confirm")
                            else:
                                expected: list[str | None] | None = None
                                if command == "expect":
                                    expected = [args[0]]
                                    if len(args) > 1:
                                        expected.append(args[1])
                                if redo:
                                    ins = lastins.copy()
                                else:
                                    ins = []
                                    print("Place your input below. After the last line, use Ctrl+C")
                                    print("--------------------")
                                    while True:
                                        try:
                                            ins.append(input())
                                        except KeyboardInterrupt:
                                            break
                                    print("--------------------")
                                    lastins = ins.copy()
                                if command == "expect":
                                    assert expected
                                    sol.expect(ins, expected)
                                else:
                                    ans = tuple(str(x).strip() for x in sol.get_solution(ins))
                                    print(f"Answers: [A] {ans[0]}, [B] {ans[1]}")
                    except:
                        print(traceback.format_exc())
        else:
            print("Available commands are select, create, delete, reset, input, expect, test, login, submit")
        previous = command


if __name__ == "__main__":
    try:
        main()
    except:
        os._exit(0)
