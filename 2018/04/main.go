package main

import (
	"bufio"
	"fmt"
	"regexp"
	"strconv"

	"os"
)

type Guard struct {
	id     int
	asleep []int
}

func getMinute(s string) int {
	re_minute := regexp.MustCompile((":(?P<min>[0-9][0-9])"))
	if !re_minute.MatchString(s) {
		panic("Kan inte matcha!!")
	}
	match := re_minute.FindStringSubmatch(s)
	minute, _ := strconv.Atoi(match[1])
	return minute
}

func main() {
	file, err := os.Open("input-sorted")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fileScanner := bufio.NewScanner(file)
	fileScanner.Split(bufio.ScanLines)

	re_guard := regexp.MustCompile("Guard #(?P<id>[0-9]+) begins shift")
	re_sleep := regexp.MustCompile("falls asleep")
	re_wake := regexp.MustCompile("wakes up")

	var guard_on_duty int
	sleep_start := -1

	//Total minutes slept for each guard
	totalsleep := make(map[int]int)

	//Minutes slept per guard
	minutes_slept := make(map[int]map[int]int)

	for fileScanner.Scan() {
		line := fileScanner.Text()
		if re_guard.MatchString(line) {
			if sleep_start >= 0 {
				panic(fmt.Sprintf("Guard #%d is still sleeping when new shift begins!", guard_on_duty))
			}
			match := re_guard.FindStringSubmatch(line)
			guard_on_duty, _ = strconv.Atoi(match[1])
			sleep_start = -1

		} else if re_sleep.MatchString(line) {
			if sleep_start >= 0 {
				panic(fmt.Sprintf("Guard #%d is still sleeping!", guard_on_duty))
			}
			sleep_start = getMinute(line)

		} else if re_wake.MatchString(line) {
			if sleep_start < 0 {
				panic(fmt.Sprintf("Guard #%d is already awake!", guard_on_duty))
			}
			sleep_end := getMinute(line)

			sleeptime := sleep_end - sleep_start

			totalsleep[guard_on_duty] += sleeptime

			if minutes_slept[guard_on_duty] == nil {
				minutes_slept[guard_on_duty] = make(map[int]int)
			}

			for min := sleep_start; min < sleep_end; min++ {
				minutes_slept[guard_on_duty][min]++
			}

			//fmt.Printf("Guard %d slept for %d minutes (%d-%d)\n", guard_on_duty, sleeptime, sleep_start, sleep_end)

			sleep_start = -1
		}

	}

	// Find the guard who slept the most
	sleepy_guard := -1
	most_slept := -1

	for guard, minutes := range totalsleep {
		if minutes > most_slept {
			sleepy_guard = guard
			most_slept = minutes
		}
	}
	//fmt.Println(totalsleep)
	fmt.Printf("Guard #%d slept the most at %d minutes\n", sleepy_guard, most_slept)

	//fmt.Println(minutes_slept[sleepy_guard])

	most_hits := 0
	var best_minute int
	for min := 0; min < 60; min++ {
		if minutes_slept[sleepy_guard][min] > most_hits {
			most_hits = minutes_slept[sleepy_guard][min]
			best_minute = min
		}
	}
	fmt.Printf("Guard #%d was most asleep during minute %d (%d times)\n", sleepy_guard, best_minute, most_hits)

	fmt.Printf("Part 1: %d\n", sleepy_guard*best_minute)

	//Find the most single slept minute of any guard
	var worstguard, worstminute, hits int

	for guard, minutes := range minutes_slept {
		for minute, count := range minutes {
			if count > hits {
				worstguard = guard
				worstminute = minute
				hits = count
			}
		}
	}
	fmt.Printf("Guard %d was asleep %d times during minute %d\n", worstguard, hits, worstminute)
	fmt.Printf("Part 2: %d\n", worstguard*worstminute)
}
