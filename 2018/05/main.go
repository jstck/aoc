package main

import (
	"fmt"
	"os"
	"strings"
)

func reduce(s string) string {
	var sb strings.Builder

	for i := 0; i < len(s); i++ {
		if i+1 < len(s) && s[i] != s[i+1] && strings.ToUpper(string(s[i])) == strings.ToUpper(string(s[i+1])) {
			//Matching pair, gets reduced, skip one
			i++
		} else {
			sb.WriteByte(s[i])
		}
	}

	return sb.String()

}

func fullyreduce(s string) (string, int) {

	newlen := len(s)
	oldlen := newlen + 1

	for newlen < oldlen {
		oldlen = newlen
		s = reduce(s)
		newlen = len(s)
	}
	return s, newlen
}

func main() {

	input, err := os.ReadFile("input")
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))
	sequence := "dabAcCaCBAcCcaDA"
	sequence = strings.TrimSpace(string(input))

	seqlen := len(sequence)

	fmt.Printf("Starting sequence: %d\n", seqlen)

	_, part1_result := fullyreduce(sequence)
	fmt.Printf("Part 1: %d\n\n", part1_result)

	charcounts := make(map[string]int)

	for _, s := range strings.Split(sequence, "") {
		charcounts[strings.ToUpper(string(s))]++
	}

	bestletter := "FOO"
	bestresult := len(sequence)
	for s := range charcounts {

		filterseq := strings.Replace(strings.Replace(sequence, s, "", -1), strings.ToLower(s), "", -1)

		_, filterresult := fullyreduce(filterseq)

		fmt.Printf("Filtering out %s, %d left, reduces to %d\n", s, len(filterseq), filterresult)
		if filterresult < bestresult {
			bestresult = filterresult
			bestletter = s
		}

	}

	fmt.Printf("Part 2: Filter out %s => %d\n", bestletter, bestresult)
}
