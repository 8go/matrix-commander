#!/usr/bin/env bash

echo "Welcome!"
echo "The script outlines the rough workflow"
echo ""
echo "You have written some code? Let's publish it."

# https://askubuntu.com/questions/1705/how-can-i-create-a-select-menu-in-a-shell-script
PS3='Please enter your choice: '
OPT1="git pull # get the latest from Github"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        break
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ" | "quit")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
OPT1="tests/test-send.py # run this testcase"
OPT2="tests/test-delete.sh # run this testcase"
OPT3="tests/test-event.sh # run this testcase"
OPT4="tests/test-rest.sh # run this testcase"
OPT5="tests/test-setget.sh # run this testcase"
OPT6="tests/test-upload.sh # run this testcase"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPT3" "$OPT4" "$OPT5" "$OPT6" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2" | "$OPT3" | "$OPT4" | "$OPT5" | "$OPT6")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        continue
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
OPT1="scripts/update-1-version.sh --mayor # increment MAJOR version number, incompatible"
OPT2="scripts/update-1-version.sh --minor # increment MINOR version number, new feature"
OPT3="scripts/update-1-version.sh --patch # increment PATCH version number, bug fix"
OPT4="scripts/update-2-help-manual.py # update help-manual file, puts it also into README.md"
OPT5="scripts/update-4-help-help.py # update help-help-pre file, puts it inte matix_commander.py"
OPT6="scripts/create-help-help.sh # update help-help file"
OPT7="scripts/create-help-usage.sh # update help-usage file"
OPT8="scripts/lintmc.sh # lint and beautify main file"
OPT9="scripts/pypi-package-1-create.sh # create PyPi release"
OPT10="scripts/pypi-package-2-publish.sh # optionally publish PyPi release; maybe skip this for minor versions; skip this if Actions workflow is preferred"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPT3" "$OPT4" "$OPT5" "$OPT6" "$OPT7" "$OPT8" "$OPT9" "$OPT10" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2" | "$OPT3" | "$OPT4" | "$OPT5" | "$OPT6" | "$OPT7" | "$OPT8" | "$OPT9" | "$OPT10")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        continue
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
OPT1="git add dist/ # must do this! commit -a will not include them"
OPT2="git status # what is the current status"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        continue
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
OPT1="git commit -a # alternative 1 for commit"
OPT2="git commit # alternative 2 for commit"
OPT3="git commit -a -m 'release: v$(cat VERSION)' # alternative 3 for commit; being lazy"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPT3" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2" | "$OPT3")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        break
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
OPT1="scripts/update-5-tag.sh # create new annotated tag"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        break
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
echo "A tag push of major version kicks off the Docker actions workflow on Github."
echo "A tag push of major version kicks off the PiPy actions workflow on Github."
echo "Note: a PR does not trigger Github Actions workflows."
echo "Only pushing a tag kicks off the workflow and only if not a minor version."
echo "Instead of 2 separate pushes, one can use *annotated* tags and ----follow-tags."
OPT1="git push --follow-tags # alternative 1; does both push of changes and push of tag"
OPT2="git push # alternative 2a; 1st push, since there is no tag, no trigger on workflows"
OPT3="git push origin v'$(cat VERSION)' # alternative 2b; 2nd push, pushing tag"
OPT4="git push && git push origin v'$(cat VERSION)' # alternative 3; both pushes"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPT3" "$OPT4" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2" | "$OPT3" | "$OPT4")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        continue
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

PS3='Please enter your choice: '
echo "Watch Actions workflows on Github, if any."
echo "Now double-check if everything is in order."
OPT1="git tag --list -n --sort=-refname # list tags"
OPT2="git log --pretty=oneline -n 7 # now it shows tag in commit hash"
OPT3="git log -1 --pretty=%B # details of last commit"
OPT4="git tag --list -n20 $(git describe) # details of last tag"
OPT5="git status # list status"
OPTC="Continue"
OPTQ="Quit"
options=("$OPT1" "$OPT2" "$OPT3" "$OPT4" "$OPT5" "$OPTC" "$OPTQ")
select opt in "${options[@]}"; do
    if [ "${REPLY,,}" == "c" ]; then opt="$OPTC"; fi
    if [ "${REPLY,,}" == "q" ]; then opt="$OPTQ"; fi
    case ${opt} in
    "$OPT1" | "$OPT2" | "$OPT3" | "$OPT4" | "$OPT5")
        OPTE=${opt%%#*} # remove everything after first #
        echo "Performing: $OPTE"
        $OPTE
        continue
        ;;
    "$OPTC")
        echo "On to next step."
        break
        ;;
    "$OPTQ")
        echo "Quitting program."
        exit 0
        ;;
    *) echo "invalid option $REPLY" ;;
    esac
done

echo "Bye"

exit 0
