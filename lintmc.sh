#!/bin/bash

# tiny 1-line script to lint matrix-commander.py

isort matrix-commander.py && flake8 matrix-commander.py && python3 -m black --line-length 79 matrix-commander.py
