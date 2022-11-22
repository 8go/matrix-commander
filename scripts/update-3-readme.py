#!/usr/bin/env python3

# - extract the README portion within the matrix_commander.py file
# - places this portion into a new separate, stand-alone README.md file
# - does a diff of previous and newly created `README.md` files to show
#   the changes

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

readmemd = "README.md"
filename = "matrix_commander/matrix_commander.py"

if isfile(filename) and access(filename, R_OK):
    # so that subprocess can execute it without PATH
    filename = "./" + filename
    readmemd = "./" + readmemd
else:
    filename = "../" + filename
    readmemd = "../" + readmemd
    if not (isfile(filename) and access(filename, R_OK)):
        print(
            f"Error: file {filename[3:]} not found, neither in "
            "local nor in parent directory."
        )
        sys.exit(1)

backupfile = readmemd + "." + date_string
shutil.copy2(readmemd, backupfile)

file = open(filename, "r").read()
m = re.search(r'"""[\s\S]*?"""', file)
if m.group(0) != "":
    text = m.group(0)
    text = text.split("\n", 5)[5]  # remove first 5 lines
    new_file = open(readmemd, "w")
    new_file.write(text.strip('"'))
    new_file.close()
    print(f"New {readmemd} was generated.")

    bashCmd = ["diff", readmemd, backupfile]
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(error)
    else:
        output = output.decode("utf-8").strip("\n")
        print(f"Diff is:\n{output}")

else:
    print(f"FAILED: No new {readmemd} was generated.")
