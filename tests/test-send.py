#!/usr/bin/python3

r"""test-send.py.
This is a simple test program.
Furthermore it is an example program demonstrating how 'matrix-commander'
can be called from a Python program.
"""

# isort: skip_file
# isort: off
from datetime import datetime
import sys
import os

# print(f"Default path is: {sys.path}")
# importing matrix_commander module
try:
    # if installed via pip
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import (
        main,
    )  # nopep8 # isort: skip
except:
    # if not installed via pip. if installed via 'git clone' or file download
    # appending a local path to sys.path
    sys.path.append("./matrix_commander")
    sys.path.append("../matrix_commander")
    # print(f"Expanded path is: {sys.path}")
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import (
        main,
    )  # nopep8 # isort: skip

now = datetime.now().strftime("%Y%m%d-%H%M%S")

# to make test self-contained, create the test file here inside Python
TESTFILE = "test.txt"
with open(TESTFILE, "w") as f:
    f.write("content of test.txt")
# set up some test arguments
print(f"Running test program: {sys.argv[0]}")
print(f"Current working directory is: {os.getcwd()}")
print(f"Path is: {sys.path}")
print(f"Arguments that are passed on to matrix-commander are: {sys.argv[1:]}")
sys.argv[0] = "matrix-commander"
sys.argv.extend(["--version"])
sys.argv.extend(["--message", f"Hello World @ {now}!"])
sys.argv.extend(["--file", TESTFILE])
sys.argv.extend(["--print-event-id"])
# sys.argv.extend(["--debug"])
# Github Action Workflow differs from local test as Github Action env
# pipes a "" into the input of the program.
print(f"Testing with these arguments: {sys.argv}")
try:
    ret = matrix_commander.main()
    if ret == 0:
        print("matrix_commander finished successfully.")
    else:
        print(
            f"matrix_commander failed with {ret} error{'' if ret == 1 else 's'}."
        )
except Exception as e:
    print(f"Exception happened: {e}")
    ret = 99
os.remove(TESTFILE)
exit(ret)
