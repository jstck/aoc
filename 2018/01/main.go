package main

import (
	//"bufio"
	"fmt"
	"strconv"
	"strings"

	//"io"
	"os"
	//"strings"
)

func main() {
	input, err := os.ReadFile("input")
	if err != nil {
		panic(err)
	}

	freq := 0
	for _, df := range strings.Split(string(input), "\n") {
		delta, _ := strconv.Atoi(df)
		freq += delta
	}

	fmt.Printf("Part 1: %d\n", freq)

	freq = 0
	freqs := make(map[int]int)
	found := false

	freqs[0] = 0

Mainloop:
	for {
		for _, df := range strings.Split(string(input), "\n") {
			delta, _ := strconv.Atoi(df)
			freq += delta
			freqs[freq]++
			if !found && freqs[freq] >= 2 {
				found = true
				fmt.Printf("Part 2: %d\n", freq)
				break Mainloop
			}

		}
	}
}
