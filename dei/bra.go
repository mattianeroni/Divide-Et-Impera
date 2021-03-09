package dei

import (
	"math"
	"math/rand"
	"sort"
)

type BRA struct {

	alpha, beta, betastart, betastep float64		// Parameters of the algorithm
	maxiter int 						// Maximum number of iterations

	solution Solution
	value, delay int

}

// Constructor
func BiasedRandomised (alpha, betastart, betastep float64, maxiter... int) *BRA{
	var iter int = 3000
	if len(maxiter) > 0 {
		iter = maxiter[0]
	}
	return &BRA{alpha, betastart, betastart,betastep, iter, nil, 0, 0}
}


// Get the solution found
func (self *BRA) getSolution () (Solution, int, int) {
	return self.solution, self.value, self.delay
}


// A Biased randomised selection based on a quasi-geometric function
func (self *BRA) biased_random_selection (size int) int {
	return int(math.Log(rand.Float64()) / math.Log(1 - self.alpha)) % size
}


// Build a new solution
func (self *BRA) buildSolution (path []*Node, dists [][]int, value int, cnode *Node) (Solution, int, int){

	// Init the part of the solution that remains the same
	index := int((1 - self.beta) * float64(len(path)))
	sol := path[:index]
	val, del := evaluate(sol, dists, value, cnode)

	// Init options and current node
	var currentNode Node = *cnode
	var newNode Node
	options := path[index:]

	// Execute a greedy construction of the new solution
	for len(options) > 0 {
		// Sort options for increasing cost (i.e., arrival + delay)
		sort.Slice(options, func (i int, j int) bool {
			return options[i].Cost(currentNode, dists, val) < options[j].Cost(currentNode, dists, val)
		})

		// Pick a new node using a quasi-geometric
		pos := self.biased_random_selection(len(options))
		newNode = *options[pos]

		// Pick the best and make it current node
		val = int(math.Max(float64(val + dists[currentNode.id][newNode.id]), float64(newNode.open)))
		del += int(math.Max(0, float64(val - newNode.close)))
		sol = append(sol, options[pos])
		currentNode = newNode
		options = append(options[:pos], options[pos + 1:]...)
	}
	// Return the new solution
	return sol, val, del
}


// Execution
func (self *BRA) execute (path []*Node, dists [][]int, value int, cnode *Node) {
	// Init starting solution
	sol, val, del := self.buildSolution(path, dists, value, cnode)

	for i := 0; i < self.maxiter; i++ {
		// Build new solution
		newsol, newval, newdel := self.buildSolution(sol, dists, value, cnode)

		// eventually update best solution found so far
		if newval + newdel < val + del {
			sol, val, del = newsol, newval, newdel
			self.beta = self.betastart
		} else {
			self.beta += self.betastep
			self.beta = math.Min(1.0, self.beta)
		}
	}

	self.solution, self.value, self.delay = sol, val, del
}
