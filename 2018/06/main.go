package main

import (
	"bufio"
	"container/list"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const test = false

type Pos struct {
	x, y int
}

func makePos(x, y int) Pos {
	var pos Pos
	pos.x = x
	pos.y = y
	return pos
}

type Grid map[Pos]int

func manhattan(pos1, pos2 Pos) int {
	dx := pos1.x - pos2.x
	dy := pos1.y - pos2.y

	if dx < 0 {
		dx = -dx
	}
	if dy < 0 {
		dy = -dy
	}

	return dx + dy
}

// Infinitely far away
const infinity = 1000000

func printGrid(grid Grid, minpos, maxpos Pos, empty string) {
	for y := minpos.y; y <= maxpos.y; y++ {
		var sb strings.Builder
		for x := minpos.x; x <= maxpos.x; x++ {
			pos := makePos(x, y)
			if grid[pos] != 0 {
				sb.WriteString(fmt.Sprintf("%d", grid[pos]%10))
			} else {
				sb.WriteString(empty)
			}
		}
		fmt.Println(sb.String())
	}
}

func neighbours(pos Pos) []Pos {
	up := makePos(pos.x, pos.y-1)
	down := makePos(pos.x, pos.y+1)
	left := makePos(pos.x-1, pos.y)
	right := makePos(pos.x+1, pos.y)

	return []Pos{up, down, left, right}
}

func inbounds(pos, min, max Pos) bool {
	if pos.x < min.x {
		return false
	}
	if pos.x > max.x {
		return false
	}
	if pos.y < min.y {
		return false
	}
	if pos.y > max.y {
		return false
	}

	return true
}

// Floodfill from a target starting point.
// Return the number of squares filled, or <0 if infinite
func floodfill(grid Grid, target Pos, minpos Pos, maxpos Pos) int {
	count := 0
	color := grid[target]

	visited := make(map[Pos]bool)
	queue := list.New()

	queue.PushBack(target)

	for queue.Len() > 0 {

		// Grab first element
		el := queue.Front()
		pos := el.Value.(Pos)
		queue.Remove(el)

		//Already been here (shouldn't happen?)
		if visited[pos] {
			continue
		}

		//Mark visited (even if it's the "wrong color")
		visited[pos] = true

		//Not the color we're looking for
		if grid[pos] != color {
			continue
		}

		//Found a new square!
		count++

		//Enqueue all neighbours
		for _, neigh := range neighbours(pos) {
			if !inbounds(neigh, minpos, maxpos) {
				if test {
					fmt.Printf("Area #%d reaches edge!\n", color)
				}
				return -1
			}
			if visited[neigh] {
				continue
			}

			queue.PushBack(neigh)
		}

	}

	if test {
		fmt.Printf("Area #%d has size %d\n", color, count)
	}
	return count

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

	maxX, maxY := 0, 0
	minX, minY := infinity, infinity

	var targets []Pos

	grid := make(Grid)

	for fileScanner.Scan() {
		line := fileScanner.Text()
		bits := strings.SplitN(line, ",", 2)

		x, _ := strconv.Atoi(strings.TrimSpace(bits[0]))
		y, _ := strconv.Atoi(strings.TrimSpace(bits[1]))

		pos := makePos(x, y)

		// Get bounding box of coordinates
		if x > maxX {
			maxX = x
		}
		if y > maxY {
			maxY = y
		}

		if x < minX {
			minX = x
		}
		if y < minY {
			minY = y
		}

		targets = append(targets, pos)
	}

	for id, target := range targets {
		grid[target] = id
	}
	//Have things start at (0,0) if appropriate
	if minX < 10 {
		minX = min(minX, 0)
	}

	if minY < 10 {
		minY = min(minY, 0)
	}

	minPos := makePos(minX, minY)
	maxPos := makePos(maxX, maxY)

	if test {
		printGrid(grid, minPos, maxPos, ".")
	}

	// Check each empty spot and see which target is closest
	for y := minPos.y; y <= maxPos.y; y++ {
		for x := minPos.x; x <= maxPos.x; x++ {
			pos := makePos(x, y)
			if grid[pos] != 0 {
				continue
			}

			var besttarget int
			bestdistance := infinity
			var border bool

			for n, targetpos := range targets {
				target_distance := manhattan(pos, targetpos)
				if target_distance < bestdistance {
					besttarget = n
					bestdistance = target_distance
					border = false
				} else if target_distance == bestdistance {
					//Something else is as good as best match yet
					border = true
				}
			}

			//Mark result in map
			if border {
				grid[pos] = -1
			} else {
				grid[pos] = besttarget
			}
		}
	}

	//printGrid(grid, minPos, maxPos, " ")

	//For each target, flood fill and see if we hit the edge (in which case the area is infinite, since there will always be a straight
	//line out to infinity where there is no closer target) or we find a bounded area, the size of which we want to know

	largest := 0
	for _, target := range targets {
		area := floodfill(grid, target, minPos, maxPos)
		if area > largest {
			largest = area
		}
	}

	fmt.Printf("Part 1: %d\n", largest)

	//Part 2. for each grid position, mark those that are within appropriate distance from all targets
	max_distance := 10000

	//test data
	if test {
		max_distance = 32
	}

	grid2 := make(Grid)
	var sample Pos
	for y := minPos.y; y <= maxPos.y; y++ {
		for x := minPos.x; x <= maxPos.x; x++ {
			pos := makePos(x, y)
			distance_sum := 0

			for _, target := range targets {
				distance_sum += manhattan(pos, target)
			}

			if distance_sum < max_distance {
				grid2[pos] = 1
				sample = pos //Save a sample for later
			}
		}
	}
	if test {
		printGrid(grid2, minPos, maxPos, ".")
	}

	//Floodfill from some element part of nice set
	area2 := floodfill(grid2, sample, minPos, maxPos)

	fmt.Printf("Part 2: %d\n", area2)

}
