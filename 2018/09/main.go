package main

import (
	"container/heap"
	"fmt"
)

type Node struct {
	value int
	left  *Node
	right *Node
}

func playmarbles(players, maxmarble int) int {
	nextmarble := 0 //Next marble to draw from the "unused pile"
	remarble := &IntHeap{}
	heap.Init(remarble)

	done := false

	for !done {
		//Get next marble
		if remarble.Len() > 0 {
			marble := nextmarble
			if marble > maxmarble {
				done = true
				continue
			}
			nextmarble++
		}
	}

	return 0

}

func main() {

	inputs := [][]int{
		{10, 1618, 8317},
		{13, 7999, 146373},
		{17, 1104, 2764},
		{21, 6111, 54718},
		{30, 5807, 37305},
		//{491, 71058, 0},
	}

	for i := 0; i < len(inputs); i++ {
		input := inputs[i]
		players := input[0]
		maxmarble := input[1]
		maxscore := input[2]

		score := playmarbles(players, maxmarble)

		if maxscore > 0 {
			if score == maxscore {
				fmt.Printf("Test %d OK\n", i)
			} else {
				fmt.Printf("Test %d FAILED. Expected:%d Got:%d\n", i, score, maxscore)
			}
		} else {
			fmt.Println("Part 1:", score)
		}
	}

}
