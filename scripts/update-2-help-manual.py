#!/usr/bin/env python3

# - runs `matrix_commander.py --manual` and writes the output into `help.manual.txt` file
# - replace this pattern:
#   ```
#   usage: ...
#   ```
#   in the README.md file with the content of the
#   newly created `help.manual.txt` file
# - runs a diff on the previous and new README.md to show the changes


import re
import shutil
import subprocess
import sys
from datetime import datetime
from os import R_OK, access
from os.path import isfile

# datetime object containing current date and time
now = datetime.now()
date_string = now.strftime("%Y%m%d-%H%M%S")

helpfile = "help.manual.txt"
filename = "README.md"
executable = "matrix_commander/matrix-commander"

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
    bashCmd = [executable, "--manual"]
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
        r"\n# Usage\n```\n[\s\S]*?```",
        r"\n# Usage\n```\n"
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
