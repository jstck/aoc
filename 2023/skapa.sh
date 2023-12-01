#!/bin/bash

DAY=$(echo $1 | sed 's/^0*//')

if [ -f "${DAY}/run.py" ]; then
    echo "${DAY}/run.py already exists!"
    exit 1
fi

mkdir ${DAY}

cp templates/aoc.py ${DAY}/run.py
cp templates/part_one.py ${DAY}/part_one.py
cp templates/part_two.py ${DAY}/part_two.py


COOKIE=$(cat cookies.txt)
URL="https://adventofcode.com/2023/day/${DAY}/input"

USER_AGENT="https://github.com/jstck/aoc/blob/master/2023/skapa.sh by john.stack@gmail.com"

curl -A "${USER_AGENT}" -o ${DAY}/input.txt -b ${COOKIE} ${URL}

cd ${DAY}