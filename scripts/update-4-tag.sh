#!/usr/bin/env bash

# commit first
echo "it is assumed that a git commit has just been committed"

# then tag
# # lightweight tag (will not be automatically pushed with --follow-tags)
# git tag v"$(cat VERSION)" # lightweight tag (will not be automatically pushed)
# annotated tag (will be automatically pushed with --follow-tags)
git tag -a -m "release: v$(cat VERSION)" -m "" -m "$(git log -1 --pretty=%B)" v"$(cat VERSION)" # annotated tag

git tag --list -n | tail -n 7 # list tags
git log --pretty=oneline -n 7 # now it shows tag in commit hash

git tag --list -n10 | tail -n 10 # show the commit comments in last tag
# git tag --list -n20 $(git describe) # show last tag details

# then push
echo "new tag was created, now ready for a git push"
