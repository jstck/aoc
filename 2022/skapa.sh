#!/bin/bash

DAY=$1

if [ -f "${DAY}/run.py" ]; then
    echo "${DAY} already exists!"
    exit 1
fi

mkdir ${DAY}

cp skeletor.py ${DAY}/run.py

DAY2=$(echo $DAY | sed 's/^0*//')

COOKIE=$(cat cookies.txt)
URL="https://adventofcode.com/2022/day/${DAY2}/input"


curl -o ${DAY}/input.txt -b ${COOKIE} ${URL}

cd ${DAY}