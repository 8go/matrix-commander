#!/usr/bin/python3

r"""test-send.py.

This is a simple test program.
Furthermore it is an example program demonstrating how 'matrix-commander'
can be called from a Python program.

"""

# isort: skip_file
# isort: off
from os.path import isfile
from os import R_OK, access
from datetime import datetime
import subprocess
import shutil
import re
import sys

# importing matrix_commander module
try:
    # if installed via pip
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import main  # nopep8 # isort: skip
except:
    # not installed via pip. installed via 'git clone' or file download
    # appending a local path to sys.path
    sys.path.append("matrix_commander")
    sys.path.append("../matrix_commander")
    import matrix_commander  # nopep8 # isort: skip
    from matrix_commander import main  # nopep8 # isort: skip

# set up some test arguments
sys.argv.extend(["--version"])
sys.argv.extend(["--message", "Hello World!"])
sys.argv.extend(["--image", "tests/test.s.png"])
print(f"Testing with these arguments: {sys.argv}")
matrix_commander.main()
