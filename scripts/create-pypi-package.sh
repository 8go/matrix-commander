#!/bin/bash

#
# # on PC where PyPi package is to be created
# python3 -m pip install --upgrade build # install necessary build packages
# rm dist/*                              # cleanup
# nano setup.cfg                         # increment version number
# python3 -m build                       # build PyPi package
# python3 -m twine upload dist/*         # upload PyPi package, use __token__ as user
#
# # on PC where to install
# sudo apt install libolm-dev
# pip3 install matrix-commander
# export PATH=$PATH:/home/user/.local/bin
# matrix-commander --help # test it
#

# prepare-commit, including version increase in setup.cfg
rm dist/* # cleanup
python3 -m build && python3 -m twine upload dist/*
