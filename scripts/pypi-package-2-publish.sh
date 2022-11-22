#!/usr/bin/env bash

# see also pypi-package-1-create.sh script which creates the PyPi release

echo "Use __token__ as user."
python3 -m twine upload dist/*
