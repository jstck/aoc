#!/bin/bash

DAY=$1

if [ -f "${DAY}/run.py" ]; then
    echo "${DAY}/run.py already exists!"
    exit 1
fi

mkdir ${DAY}

cp template.py ${DAY}/run.py

DAY2=$(echo $DAY | sed 's/^0*//')

COOKIE=$(cat cookies.txt)
URL="https://adventofcode.com/2022/day/${DAY2}/input"

USER_AGENT="https://github.com/jstck/aoc/blob/master/2022/skapa.sh by john.stack@gmail.com"

curl -A "${USER_AGENT}" -o ${DAY}/input.txt -b ${COOKIE} ${URL}

cd ${DAY}