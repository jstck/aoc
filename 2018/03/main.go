package main

import (
	"bufio"
	"fmt"
	"regexp"
	"strconv"

	"os"
)

type Pos struct {
	x, y int
}

type Claim struct {
	id, x, y, w, h int
}

func parseClaim(line string) Claim {
	re_claim := regexp.MustCompile("^#(?P<i>[0-9]+) @ (?P<x>[0-9]+),(?P<y>[0-9]+): (?P<w>[0-9]+)x(?P<h>[0-9]+)$")
	match := re_claim.FindStringSubmatch(line)
	cmap := make(map[string]int)
	for i, name := range re_claim.SubexpNames() {
		if i > 0 && i <= len(match) {
			cmap[name], _ = strconv.Atoi(match[i])
		}
	}

	var claim Claim

	claim.id = cmap["i"]
	claim.x = cmap["x"]
	claim.y = cmap["y"]
	claim.w = cmap["w"]
	claim.h = cmap["h"]

	return claim
}

func main() {
	file, err := os.Open("input")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fileScanner := bufio.NewScanner(file)
	fileScanner.Split(bufio.ScanLines)

	//#13 @ 928,664: 18x15
	var claims []Claim

	for fileScanner.Scan() {
		line := fileScanner.Text()
		claim := parseClaim(line)
		claims = append(claims, claim)
	}

	grid := make(map[Pos]int)

	for _, claim := range claims {

		// fmt.Printf("Marking claim #%d...", claim.id)

		//Mark in grid
		c := 0
		for x := claim.x; x < claim.x+claim.w; x++ {
			for y := claim.y; y < claim.y+claim.h; y++ {
				var p Pos
				p.x, p.y = x, y
				grid[p]++
				c++
			}
		}
		// fmt.Printf("%d squares claimed\n", c)

	}

	// fmt.Printf("Tallying...\n")

	multicount := 0

	//Scan and tally up the grid
	for _, count := range grid {
		if count > 1 {
			multicount++
		}
	}
	fmt.Printf("Part 1: %d\n", multicount)

nextclaim:
	for _, claim := range claims {
		//Check to see if this claim has any overlaps (if not, all squares are 1)
		for x := claim.x; x < claim.x+claim.w; x++ {
			for y := claim.y; y < claim.y+claim.h; y++ {
				var p Pos
				p.x, p.y = x, y
				if grid[p] != 1 {
					//fmt.Printf("Claim #%d has overlap at %d, %d (%d)!\n", claim.id, p.x, p.y, grid[p])
					continue nextclaim
				}
			}
		}
		fmt.Printf("Part 2: Claim #%d has no overlap!\n", claim.id)
		// fmt.Printf("%d squares claimed\n", c)

	}

}
