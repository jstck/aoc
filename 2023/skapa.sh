#!/bin/bash


if [ $# -eq 0 ]
then
  DAY0=$(date "+%d")
  DAY=$(echo $DAY0 | sed 's/^0*//')
else
  DAY=$(echo $1 | sed 's/^0*//')
  DAY0=$(echo "0${DAY}"| sed -E 's/.*(..)/\1/')
fi

if [ -d "${DAY0}" ]; then
    echo "${DAY0} already exists!"
    exit 1
fi

mkdir ${DAY0}

cp templates/plain_template.py ${DAY0}/solution.py

COOKIE=$(cat cookies.txt)
URL="https://adventofcode.com/2023/day/${DAY}/input"

USER_AGENT="https://github.com/jstck/aoc/blob/master/2023/skapa.sh by john.stack@gmail.com"

curl -A "${USER_AGENT}" -o ${DAY0}/input.txt -b ${COOKIE} ${URL}

cd ${DAY0}
