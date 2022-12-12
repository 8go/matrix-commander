#!/usr/bin/env python3

# - runs `create-help-help-pre.sh` to create output file `help.help.pre.txt`
# - replace this pattern:
#   ```
#   usage: ...
#   ```
#   in the matrix_commander.py file with the content of the
#   newly created `help.help.pre.txt` file
# - runs a diff on the previous and new matrix_commander.py to show the changes


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

helpfile = "help.help.pre.txt"
filename = "matrix_commander/matrix_commander.py"
executable = "scripts/create-help-help-pre.sh"

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

bashCmd = [executable, "--ignored"]
process = subprocess.Popen(bashCmd, stdout=sys.stdout)
output, error = process.communicate()
if error:
    print(error)
else:
    print(f"Output of {executable} is {output}.")

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
        r'help_help_pre = f"""\n[\s\S]*?"""',
        'help_help_pre = f"""\n'
        + helptext.translate(
            str.maketrans(
                {
                    "\\": r"\\",
                }
            )
        )
        + '"""',
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
