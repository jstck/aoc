package main

import (
	"bufio"
	"fmt"

	//"io"
	"os"
	"strings"
)

func countchars(s string) map[string]int {
	f := make(map[string]int)

	for _, c := range strings.Split(s, "") {
		f[c]++
	}

	return f
}

func countstuff(f map[string]int) (int, int) {
	twos, threes := 0, 0

	for _, count := range f {
		if count == 2 {
			twos++
		} else if count == 3 {
			threes++
		}
	}

	return twos, threes
}

func countdiff(s1, s2 string) int {
	if len(s1) != len(s2) {
		panic("Strings of different lengths!!!")
	}

	diff := 0

	for i := 0; i < len(s1); i++ {
		if s1[i] != s2[i] {
			diff++
		}
	}

	return diff
}

func samechars(s1, s2 string) string {
	out := ""

	for i := 0; i < len(s1); i++ {
		if s1[i] == s2[i] {
			out = out + string(s1[i])
		}
	}
	return out
}

func main() {
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fileScanner := bufio.NewScanner(file)
	fileScanner.Split(bufio.ScanLines)

	sum2, sum3 := 0, 0

	var boxes []string

	for fileScanner.Scan() {
		line := fileScanner.Text()
		boxes = append(boxes, line)
		freqs := countchars(line)
		twos, threes := countstuff(freqs)

		if twos > 0 {
			sum2++
		}
		if threes > 0 {
			sum3++
		}
	}

	fmt.Printf("Part 1: %d\n", sum2*sum3)

	best := 9999
	var best_n1, best_n2 int

	// Compare all pairs of strings
	for n1 := 0; n1 < len(boxes)-1; n1++ {
		for n2 := n1 + 1; n2 < len(boxes); n2++ {
			d := countdiff(boxes[n1], boxes[n2])
			if d < best {
				fmt.Printf("New best %d %d -> %d\n", n1, n2, d)
				best = d
				best_n1, best_n2 = n1, n2
			}
		}
	}

	fmt.Printf("Part 2: %s\n", samechars(boxes[best_n1], boxes[best_n2]))
}
