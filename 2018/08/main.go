package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const test = false

type Node struct {
	metadata []int
	children []*Node
}

func makeNode(ch chan int) Node {
	nChildren := <-ch
	nMetadata := <-ch

	var node Node

	//Read children recursively
	for n := 0; n < nChildren; n++ {
		child := makeNode(ch)
		node.children = append(node.children, &child)
	}

	//Read metadata
	for n := 0; n < nMetadata; n++ {
		meta := <-ch
		node.metadata = append(node.metadata, meta)
	}

	return node
}

func sumMetadata(node Node) int {
	sum := 0
	for _, x := range node.metadata {
		sum += x
	}

	for _, c := range node.children {
		sum += sumMetadata(*c)
	}

	return sum

}

func sumValues(node Node) int {
	sum := 0

	if len(node.children) == 0 {
		return sumMetadata(node)
	}

	for _, x := range node.metadata {

		//Skip nonexistent children
		if x <= 0 || x > len(node.children) {
			continue
		}

		//This should be caching stuff, but seems to do fine without.
		sum += sumValues(*node.children[x-1])
	}

	return sum

}

func main() {
	var input string
	if test {
		input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
	} else {
		in_bytes, err := os.ReadFile("input")
		if err != nil {
			panic(err)
		}
		input = strings.TrimSpace(string(in_bytes))
	}
	tokens := strings.Split(input, " ")

	datachan := make(chan int, len(tokens))

	for _, token := range tokens {
		x, err := strconv.Atoi(token)
		if err != nil {
			panic(err)
		}

		datachan <- x

	}

	root := makeNode(datachan)
	fmt.Println("Part 1: ", sumMetadata(root))
	fmt.Println("Part 2: ", sumValues(root))
}
