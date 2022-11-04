#!/usr/bin/env python3
import re
import shutil
import subprocess
import sys
from datetime import datetime
from os import R_OK, access
from os.path import isfile

# replace this pattern:
# ```
# usage: ...
# ```
# in the matrix_commander.py file with the output of
# matrix_commander.py --help

# datetime object containing current date and time
now = datetime.now()
date_string = now.strftime("%Y%m%d-%H%M%S")

helpfile = "help.txt"
filename = "matrix_commander/matrix_commander.py"

if isfile(filename) and access(filename, R_OK):
    # so that subprocess can execute it without PATH
    filename = "./" + filename
    helpfile = "./" + helpfile
else:
    filename = "../" + filename
    helpfile = "../" + helpfile
    if not (isfile(filename) and access(filename, R_OK)):
        print(
            f"Error: file {filename[3:]} not found, neither in "
            "local nor in parent directory."
        )
        sys.exit(1)

backupfile = filename + "." + date_string
shutil.copy2(filename, backupfile)

with open(helpfile, "w") as f:
    # tty size defaults to 80 columns
    bashCmd = [filename, "--help"]
    process = subprocess.Popen(bashCmd, stdout=f)
    _, error = process.communicate()
    if error:
        print(error)

bashCmd = ["wc", "-L", helpfile]  # max line length
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()
if error:
    print(error)
else:
    output = output.decode("utf-8").strip("\n")
    print(f"Maximum line length is {output}")

with open(helpfile, "r+") as f:
    helptext = f.read()
    print(f"Length of new {helpfile} file is: {len(helptext)}")

with open(filename, "r+") as f:
    text = f.read()
    print(f"Length of {filename} before: {len(text)}")
    text = re.sub(
        r"```\nusage: [\s\S]*?```",
        "```\n"
        + helptext.translate(
            str.maketrans(
                {
                    "\\": r"\\",
                }
            )
        )
        + "```",
        text,
    )

    print(f"Length of {filename} after:  {len(text)}")
    f.seek(0)
    f.write(text)
    f.truncate()

bashCmd = ["diff", filename, backupfile]
process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
output, error = process.communicate()
if error:
    print(error)
else:
    output = output.decode("utf-8").strip("\n")
    print(f"Diff is:\n{output}")
