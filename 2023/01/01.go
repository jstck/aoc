package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var digits = map[string]string{
	"zero":  "z0o",
	"one":   "o1e",
	"two":   "t2o",
	"three": "t3e",
	"four":  "f4r",
	"five":  "f5e",
	"six":   "s6x",
	"seven": "s7n",
	"eight": "e8t",
	"nine":  "n9e",
}

func read_input() []string {
	var lines []string
	fp, err := os.Open("input.txt")

	if err != nil {
		panic(err)
	}

	defer fp.Close()

	scanner := bufio.NewScanner(fp)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if len(line) > 0 {
			lines = append(lines, line)
		}
	}

	return lines

}

func main() {
	input := read_input()

	var part1_score int
	var part2_score int

	r_left := regexp.MustCompile("^\\D*(\\d)")
	r_right := regexp.MustCompile("(\\d)\\D*$")

	for _, s := range input {

		left1, _ := strconv.Atoi(r_left.FindStringSubmatch(s)[1])
		right1, _ := strconv.Atoi(r_right.FindStringSubmatch(s)[1])

		score1 := 10*left1 + right1

		//Transmogrify digits
		for a, b := range digits {
			s = strings.Replace(s, a, b, -1)
		}

		left2, _ := strconv.Atoi(r_left.FindStringSubmatch(s)[1])
		right2, _ := strconv.Atoi(r_right.FindStringSubmatch(s)[1])

		score2 := 10*left2 + right2

		part1_score += score1
		part2_score += score2

	}

	fmt.Println("Part 1: ", part1_score)
	fmt.Println("Part 2: ", part2_score)

}
