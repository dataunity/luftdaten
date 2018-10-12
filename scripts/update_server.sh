#!/bin/bash


# ************* Arguments *************

# Script template from: https://stackoverflow.com/a/29754866

# saner programming env: these switches turn some bugs into errors
set -o errexit -o pipefail -o noclobber -o nounset

! getopt --test > /dev/null
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi

OPTIONS=dfo:r:v
LONGOPTS=debug,force,output:,root:,verbose

# -use ! and PIPESTATUS to get exit code with errexit set
# -temporarily store output to be able to check for errors
# -activate quoting/enhanced mode (e.g. by writing out “--options”)
# -pass arguments only via   -- "$@"   to separate them correctly
! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    # e.g. return value is 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi
# read getopt’s output this way to handle the quoting right:
eval set -- "$PARSED"

d=y f=n v=n outFile=- r=..
# now enjoy the options in order and nicely split until we see --
while true; do
    case "$1" in
        -d|--debug)
            d=y
            shift
            ;;
        -f|--force)
            f=y
            shift
            ;;
        -v|--verbose)
            v=y
            shift
            ;;
        -o|--output)
            outFile="$2"
            shift 2
            ;;
        -r|--root)
            r="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

# handle non-option arguments
#if [[ $# -ne 1 ]]; then
#    echo "$0: A single input file is required."
#    exit 4
#fi
#echo "not optional arg: $1"


# ************* Script *************

root_dir="$r"
script_dir="${root_dir}/scripts"
python_exe="${root_dir}/env/bin/python"

echo "verbose: $v, force: $f, debug: $d, out: $outFile r: $r"
echo "$root_dir $script_dir"


#if [ ! -f "id_rsa" ]; then \
#    echo "Missing private SSH key for syncing with GitHub (id_rsa)."; \
#    echo "Generate a private key for your GitHub account and place it in the root dir."; \
#    exit 1; \
#fi

if [ ! -f $python_exe ]; then \
    echo "Couldn't find the python executeable. Generate Python virtual environment, as per the README."; \
    exit 1; \
fi

cd $script_dir

$python_exe -c "print('hello')"

bash dummy.sh
#$python_exe download_data.py
#$python_exe process_data.py
# TODO: add files under data/luftdaten/aggregated
# TODO: commit
# TODO: push