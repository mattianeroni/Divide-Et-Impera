package dei

import (
	"math"
	"math/rand"
)



// Solution type
type Solution []*Node



// Evaluate a solution
func evaluate (sol Solution, dists [][]int, value int, cnode *Node) (int, int) {
	var val, del = value, 0
	var currentNode Node = *cnode
	for _, node := range sol {
		val = int(math.Max(float64(val + dists[currentNode.id][node.id]), float64(node.open)))
		del += int(math.Max(0, float64(val - node.close)))
		currentNode = *node
	}
	return val, del
}






// divide et impera algorithm
type DivideEtImpera struct {

	dists [][]int 				// The distance matrix
	current Solution			// The current solution under construction
	value, delay int 			// Value and delay of the current solution
	cnode *Node 				// The current node, i.e., the last node of the solution under construction

	p, maxsplit int 			// Parameters of the algorithm

	alg Algorithm 				// The incorporated algorithm

}


// Constructor
func DEI (alg Algorithm, dists[][]int, p, maxsplit int) *DivideEtImpera {
	return &DivideEtImpera{dists, make([]*Node,0), 0, 0,nil, p, maxsplit, alg}
}


// Solve a subpath using the incorporated algorithm
func (self *DivideEtImpera) Solve (path []*Node) {
	// Execute the algorithm incorporated and get the solution found
	self.alg.execute (path, self.dists, self.value, self.cnode)
	sol, v, d := self.alg.getSolution()
	// Update the solution
	self.current = append(self.current, sol...)
	self.value = v
	self.delay += d
	self.cnode = sol[len(sol) - 1]
}



func (self *DivideEtImpera) Execute (path []*Node) (Solution, int, int){
	// Set the current node if not defined yet
	if self.cnode == nil {
		self.cnode = path[0]
		path = path[1:]
	}

	if len(path) > self.p {
		// Try to split the path
		pivot := path[rand.Intn(len(path))]
		var first = make([]*Node, 0)
		var second = make([]*Node, 0)
		var split int = 0
		for (len(first) == 0 || len(second) == 0) && split < self.maxsplit{
			split++
			for _, node := range path {
				if node.close < pivot.open {
					first = append(first, node)
				} else {
					second = append(second, node)
				}
			}
		}

		// If we have not been able to split, the path is solved as is using
		// the incorporated algorithm
		if len(first) == 0 || len(second) == 0 {
			self.Solve (path)
		} else {
			// Otherwise split again recursively
			self.Execute(first); self.Execute(second)
		}

	} else {
		// If the path is not too long, solve it with the incorporated algorithm
		self.Solve(path)
	}

	// Returns the solution
	return self.current, self.value, self.delay
}
