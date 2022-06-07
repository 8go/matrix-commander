#!/bin/bash

# commit first

# then tag
git tag v"$(cat VERSION)"
git tag --list -n | head -n 7        # list tags
git log --pretty=oneline | head -n 7 # now it shows tag in commit hash

# then push
