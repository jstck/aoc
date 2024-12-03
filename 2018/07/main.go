package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"sort"
	"strings"
)

const test = false

type Node struct {
	id       string
	parents  []string
	children []string
}

// Only one parent or child known when creating a node
func makeNode(id, parent, child string) Node {
	var node Node

	node.id = id
	if parent != "" {
		node.parents = append(node.parents, parent)
	}
	if child != "" {
		node.children = append(node.children, child)
	}

	return node
}

func main() {
	filename := "input"
	if test {
		filename = "test-input"
	}

	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fileScanner := bufio.NewScanner(file)
	fileScanner.Split(bufio.ScanLines)

	re_line := regexp.MustCompile("^Step (?P<a>[A-Z]) must be finished before step (?P<a>[A-Z]) can begin.$")

	graph := make(map[string]Node)
	var ids []string

	for fileScanner.Scan() {
		line := fileScanner.Text()
		match := re_line.FindStringSubmatch(line)
		a := match[1]
		b := match[2]

		fmt.Printf("%s -> %s\n", a, b)

		parent := graph[a]
		child := graph[b]

		parent.children = append(parent.children, b)
		child.parents = append(child.parents, a)

		//New node
		if parent.id == "" {
			parent.id = a
			ids = append(ids, a)
		}

		if child.id == "" {
			child.id = b
			ids = append(ids, b)
		}

		graph[a] = parent
		graph[b] = child
	}

	fmt.Println(graph)

	/*
		var start, end string

		//Find start and end nodes
		for _, node := range graph {
			if len(node.parents) == 0 {
				if start != "" {
					fmt.Printf("Multipe start nodes found (%s and %s)\n", start, node.id)
				}
				start = node.id
			}
			if len(node.children) == 0 {
				if end != "" {
					fmt.Printf("Multipe end nodes found (%s and %s)\n", end, node.id)
				}
				end = node.id
			}
		}

		fmt.Println("Start:", start)
		fmt.Println("End:", end)
	*/

	made := make(map[string]bool)
	sort.Sort(sort.StringSlice(ids))

	fmt.Println(ids)

	var result strings.Builder
	for len(made) < len(ids) {
		//Find first thing that is "makeable"
	nextthing:
		for _, id := range ids {
			if made[id] {
				continue
			}
			thing := graph[id]
			for _, parent := range thing.parents {
				if !made[parent] {
					continue nextthing
				}
			}

			//Thing can be made
			//fmt.Println("Making", id)
			made[id] = true
			result.WriteString(id)
			break
		}
	}

	fmt.Printf("Part 1: %s\n", result.String())

}
