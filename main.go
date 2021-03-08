package main

import (
	"bufio"
	"divide-et-impera/dei"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
	"math/rand"
)


func main () {

	// Set a random seed
	rand.Seed(time.Now().UnixNano())

	for _, filename := range benchmarks {
		nodes := readfile (filename)
		dists := distance_matrix (nodes)

		bra := dei.BiasedRandomised(0.9, 0.1, 0.1, 3000)
		d := dei.DEI(bra, dists, 30, 1000)

		start := time.Now()
		_, value, delay := d.Execute(nodes)
		elapsed := time.Now().Sub(start)

		fmt.Print("BRA - ", filename, " - ", value, " - ", delay, " - ", elapsed, "\n")

		pso := dei.ParticleSwarm(0.9, 0.02, 3000, 1000, 30)
		d = dei.DEI(pso, dists, 30, 1000)

		start = time.Now()
		_, value, delay = d.Execute(nodes)
		elapsed = time.Now().Sub(start)

		fmt.Print("PSO - ", filename, " - ", value, " - ", delay, " - ", elapsed, "\n")

	}
}

// Benchmarks problems
var benchmarks = [100]string {
"n200w100.001.txt",  "n250w100.001.txt",  "n300w100.001.txt",  "n400w100.001.txt",
"n200w100.002.txt",  "n250w100.002.txt",  "n300w100.002.txt",  "n400w100.002.txt",
"n200w100.003.txt",  "n250w100.003.txt",  "n350w100.003.txt",  "n400w100.003.txt",
"n200w100.004.txt",  "n250w100.004.txt",  "n350w100.004.txt",  "n400w100.004.txt",
"n200w100.005.txt",  "n250w100.005.txt",  "n350w100.005.txt",  "n400w100.005.txt",
"n200w200.001.txt",  "n250w200.001.txt",  "n350w200.001.txt",  "n400w200.001.txt",
"n200w200.002.txt",  "n250w200.002.txt",  "n350w200.002.txt",  "n400w200.002.txt",
"n200w200.003.txt",  "n250w200.003.txt",  "n350w200.003.txt",  "n400w200.003.txt",
"n200w200.004.txt",  "n250w200.004.txt",  "n350w200.004.txt",  "n400w200.004.txt",
"n200w200.005.txt",  "n250w200.005.txt",  "n350w200.005.txt",  "n400w200.005.txt",
"n200w300.001.txt",  "n250w300.001.txt",  "n350w300.001.txt",  "n400w300.001.txt",
"n200w300.002.txt",  "n250w300.002.txt",  "n350w300.002.txt",  "n400w300.002.txt",
"n200w300.003.txt",  "n250w300.003.txt",  "n350w300.003.txt",  "n400w300.003.txt",
"n200w300.004.txt",  "n250w300.004.txt",  "n350w300.004.txt",  "n400w300.004.txt",
"n200w300.005.txt",  "n250w300.005.txt",  "n350w300.005.txt",  "n400w300.005.txt",
"n200w400.001.txt",  "n250w400.001.txt",  "n350w400.001.txt",  "n400w400.001.txt",
"n200w400.002.txt",  "n250w400.002.txt",  "n350w400.002.txt",  "n400w400.002.txt",
"n200w400.003.txt",  "n250w400.003.txt",  "n350w400.003.txt",  "n400w400.003.txt",
"n200w400.004.txt",  "n250w400.004.txt",  "n350w400.004.txt",  "n400w400.004.txt",
"n200w400.005.txt",  "n250w400.005.txt",  "n350w400.005.txt",  "n400w400.005.txt",
"n200w500.001.txt",  "n250w500.001.txt",  "n350w500.001.txt",  "n400w500.001.txt",
"n200w500.002.txt",  "n250w500.002.txt",  "n350w500.002.txt",  "n400w500.002.txt",
"n200w500.003.txt",  "n250w500.003.txt",  "n350w500.003.txt",  "n400w500.003.txt",
"n200w500.004.txt",  "n250w500.004.txt",  "n350w500.004.txt",  "n400w500.004.txt",
"n200w500.005.txt",  "n250w500.005.txt",  "n350w500.005.txt",  "n400w500.005.txt"}


// Translate a file into a problem
func readfile (filename string) []*dei.Node {
	var nodes = make([]*dei.Node, 0)

	// Open the file
	file, err := os.Open("./benchmarks/" + filename)
	if err != nil {
		panic("File not found.")
	}
	defer file.Close()

	// Read line by line and make a Node for each line
	scanner := bufio.NewScanner(file)
	var i int = 0
	for scanner.Scan() {
		if i > 0 {
			tokens := strings.Fields(scanner.Text())
			id, _ := strconv.ParseInt(tokens[0], 10, 64)
			x, _ := strconv.ParseFloat(tokens[1], 64)
			y, _ := strconv.ParseFloat(tokens[2], 64)
			open, _ := strconv.ParseFloat(tokens[4], 64)
			close, _ := strconv.ParseFloat(tokens[5], 64)
			// NOTE: Nodes id is made 0-indexed
			nodes = append(nodes, dei.NewNode(int(id - 1), int(x), int(y), int(open), int(close)))
		}
		i++
	}
	// Returns the nodes
	return nodes
}





func distance_matrix (nodes []*dei.Node) [][]int {
	matrix := make([][]int, len(nodes))
	for i, n := range nodes {
		matrix[i] = make([]int, len(nodes))
		for j, m := range nodes {
			matrix[i][j] = dei.Euclidean(*n, *m)
		}
	}
	return matrix
}
