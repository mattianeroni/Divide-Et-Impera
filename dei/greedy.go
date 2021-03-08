package dei

import (
	"math"
	"sort"
)

type Greedy struct {
	solution Solution
	value, delay int
}

// Constructor
// Just call &Greedy{}

// Get the solution
func (self *Greedy) getSolution () (Solution, int, int) {
	return self.solution, self.value, self.delay
}

// Execute
func (self *Greedy) execute (path []*Node, dists [][]int, value int, cnode *Node) {
	// Init the current node without risk of changing the pointer
	var currentNode Node = *cnode

	// Init new solution, value and delay
	var sol = make([]*Node, 0)
	var val int = value
	var d int = 0

	// Make the list of options
	var options = make([]*Node, len(path))
	copy(options, path)

	// Execute a greedy construction of the new solution
	for len(options) > 0 {
		// Sort options for increasing cost (i.e., arrival + delay)
		sort.Slice(options, func (i int, j int) bool {
			return options[i].Cost(currentNode, dists, val) < options[j].Cost(currentNode, dists, val)
		})
		// Pick the best and make it current node
		val = int(math.Max(float64(val + dists[currentNode.id][options[0].id]), float64(options[0].open)))
		d += int(math.Max(0, float64(val - options[0].close)))
		sol = append(sol, options[0])
		currentNode = *options[0]
		options = options[1:]
	}
	self.solution = sol; self.value = val; self.delay = d
}
