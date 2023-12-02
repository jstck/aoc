#!/bin/bash


DAY=$(echo $1 | sed 's/^0*//')

if [ $DAY -lt 10 ]
then
    DAY0=$(echo "0${DAY}")
else
    DAY0=$DAY
fi


if [ -f "${DAY0}/run.py" ]; then
    echo "${DAY0}/run.py already exists!"
    exit 1
fi

mkdir ${DAY0}

cp templates/*.py ${DAY0}/run.py

COOKIE=$(cat cookies.txt)
URL="https://adventofcode.com/2023/day/${DAY}/input"

USER_AGENT="https://github.com/jstck/aoc/blob/master/2023/skapa.sh by john.stack@gmail.com"

curl -A "${USER_AGENT}" -o ${DAY0}/input.txt -b ${COOKIE} ${URL}

cd ${DAY}