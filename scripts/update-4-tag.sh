#!/bin/bash

# commit first

# then tag
# # lightweight tag (will not be automatically pushed with --follow-tags)
# git tag v"$(cat VERSION)" # lightweight tag (will not be automatically pushed)
# annotated tag (will be automatically pushed with --follow-tags)
git tag -a -m "release: v$(echo VERSION)" v"$(cat VERSION)" # annotated tag

git tag --list -n | head -n 7 # list tags
git log --pretty=oneline -n 7 # now it shows tag in commit hash

# then push
