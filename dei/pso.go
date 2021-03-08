package dei

import (
	"errors"
	"math"
	"math/rand"
	"sort"
)

// *****************************************************************************************************************
//                                                      GENERAL METHODS
// *****************************************************************************************************************
// Look up for a node in a slice
func getPosition (n *Node, list []*Node) (int, error) {
	for i, node := range list {
		if node == n {
			return i, nil
		}
	}
	return -1, errors.New("Element not found in slice.")
}


// Reverse a slice
func reverse(list []*Node) []*Node {
	for i, j := 0, len(list)-1; i < j; i, j = i+1, j-1 {
		list[i], list[j] = list[j], list[i]
	}
	return list
}
// *****************************************************************************************************************
//                                                   END GENERAL METHODS
// *****************************************************************************************************************


// *****************************************************************************************************************
//                                                 PARTICLE SWARM OPTIMIZATION
// *****************************************************************************************************************
// Particle Swarm Optimization
type PSO struct {

	solution          		Solution		// The last solution found
	value, delay          		 int		// The value and the delay of the last solution
	maxiter, maxnoimp   	     int		// The maximum number of iterations and iterations without improvement
	swarm     		     []*Particle		// The swarm of particles

}




// Constructor
func ParticleSwarm (beta, deepsearch float64, maxiter, maxnoimp, particles int) *PSO {
	swarm := make ([]*Particle, particles)
	for i := 0; i < particles; i++ {
		swarm[i] = NewParticle(beta, deepsearch)
	}
	return &PSO{nil, 0, 0, maxiter, maxnoimp, swarm}
}




// Return the solution
func (self *PSO) getSolution() (Solution, int, int) {
	return self.solution, self.value, self.delay
}





// Execute
func (self *PSO) execute (path []*Node, dists [][]int, value int, cnode *Node){

	// Init the best solution
	var bestSol = make([]*Node, len(path))
	copy (bestSol, path)
	var bestVal, bestDel = evaluate(bestSol, dists, value, cnode)

	// Init the solutions of the particles
	for _, p := range self.swarm {
		p.initialize (path, dists, value, cnode)
	}

	// Init othe useful variables
	var noimp int = 0

	// Momentaneous best solution
	var newBest = make([]*Node, len(path))
	copy(newBest, path)
	var newVal, newDel = bestVal, bestDel

	// iterations
	for iter := 0; iter < self.maxiter; iter++{
		// Move the swarm
		for _, p := range self.swarm{
			sol, v, d := p.move(bestSol, bestVal, bestDel, dists, value, cnode)
			if v + d < newVal + newDel {
				newBest, newVal, newDel = sol, v, d
			}
		}

		// Update the best
		if newVal + newDel < bestVal + bestDel {
			bestSol, bestVal, bestDel = newBest, newVal, newDel
			noimp = -1
		}
		// Update iterations without improvement
		noimp++
		// Eventually exits if no improvement has been obtained for too long time
		if noimp > self.maxnoimp {
			break
		}
	}
	// Save the best solution found
	self.solution, self.value, self.delay = bestSol, bestVal, bestDel
}
// *****************************************************************************************************************
//                                               END PARTICLE SWARM
// *****************************************************************************************************************




// *****************************************************************************************************************
//                                                      SWARM
// *****************************************************************************************************************
// A particle of the particle swarm optimization
type Particle struct {

	beta, deepsearch 					 float64		// The parameter of the biased randomised selection and
														// the probability of a deepsearch.

	greedy, intention, pbest             []*Node		// The solutions considered and known by each particle
	vgreedy, vintention, vpbest				 int		// The value of the solutions above.
	dgreedy, dintention, dpbest 			 int		// The delay associated to the solutions above.

}



// Constructor
func NewParticle (beta, deepsearch float64) *Particle {
	return &Particle{beta, deepsearch,nil, nil, nil, 0, 0, 0, 0, 0, 0}
}




// A Biased randomised selection based on a quasi-geometric function
func (self *Particle) biased_random_selection (size int) int {
	return int(math.Log(rand.Float64()) / math.Log(1.0 - self.beta)) % size
}




// Initialize the particle
func (self *Particle) initialize (path []*Node, dists [][]int, value int, cnode *Node){
	// General init
	self.greedy = make([]*Node, len(path))
	self.intention = make([]*Node, len(path))
	self.pbest = make([]*Node, len(path))

	// Initialize the greedy solution
	greedy := &Greedy{}
	greedy.execute(path, dists, value, cnode)
	self.greedy, self.vgreedy, self.dgreedy = greedy.getSolution()

	// Initialize the personal best
	copy(self.pbest, path)
	rand.Shuffle(len(path), func(i, j int) {self.pbest[i], self.pbest[j] = self.pbest[j], self.pbest[i]})
	self.vpbest, self.dpbest = evaluate(self.pbest, dists, value, cnode)

	// Initialize the intention
	copy(self.intention, path)
	rand.Shuffle(len(path), func(i, j int) {self.intention[i], self.intention[j] = self.intention[j], self.intention[i]})
	self.vintention, self.dintention = evaluate(self.intention, dists, value, cnode)

}



// The movement of the particle
func (self *Particle) move (best Solution, bestVal int, bestDel int, dists[][]int, value int, cnode *Node) (Solution, int, int) {

	// Initialize the current new solution to construct
	var currentNode *Node = cnode
	var current = make([]*Node, 0)
	var val, d = value, 0

	// The list of remaining nodes to include in the new solution
	var remaining = make([]*Node, len(best))
	copy(remaining, best)

	// For each node singularly
	for j := 0; j < len(best); j++ {

		// Define the candidates to be the next node in the new solution
		var options []*Node

		if len(current) > 0 {
			// Define the possible options as next nodes
			i1, err1 := getPosition(currentNode, self.greedy)
			i2, err2 := getPosition(currentNode, self.intention)
			i3, err3 := getPosition(currentNode, self.pbest)
			i4, err4 := getPosition(currentNode, best)

			if err1 != nil {
				panic(err1)
			}
			if err2 != nil {
				panic(err2)
			}
			if err3 != nil {
				panic(err3)
			}
			if err4 != nil {
				panic(err4)
			}

			var sols = [4][]*Node{self.greedy, self.intention, self.pbest, best}
			var indexes = [4]int{i1, i2, i3, i4}
			options = make([]*Node, 0)
			for i := 0; i < 4; i++ {
				index, sol := indexes[i], sols[i]

				if index < len(best) - 1 {
					_, err := getPosition(sol[index + 1], current)
					if err != nil {
						options = append(options, sol[index + 1])
					}
				}
			}
		} else {
			// If the node is the first included it is just selected from the
			// first nodes in each solution.
			options = []*Node{self.greedy[0], self.intention[0], self.pbest[0], best[0]}
		}

		// Select the new node from the options
		var newNode *Node
		if len(options) > 0 {
			// Sort options from best to worst, and pick a node according to a quasi-geometric function
			sort.Slice(options, func(a, b int) bool {
				return options[a].Cost(*currentNode, dists, val) < options[b].Cost(*currentNode, dists, val)
			})
			newNode = options[self.biased_random_selection(len(options))]
			// Remove the node selected from the list of remainings
			p, _ := getPosition(newNode, remaining)
			remaining = append(remaining[:p], remaining[p + 1:]...)
		} else {
			// If no options are available.
			// Pick a random element and remove it from the list of remainings
			rndEl := rand.Intn(len(remaining))
			newNode = remaining[rndEl]
			remaining = append(remaining[:rndEl], remaining[rndEl + 1:]...)
		}

		// Update the value and the delay of the current solution
		val = int(math.Max(float64(val + dists[currentNode.id][newNode.id]), float64(newNode.open)))
		d += int(math.Max(0, float64(val - newNode.close)))
		// Update the current solution and make the selected node the current node
		current = append(current, newNode)
		currentNode = newNode
	}

	// Update the intention
	copy(self.intention, current)
	rand.Shuffle(len(current), func(i, j int) { self.intention[i], self.intention[j] = self.intention[j], self.intention[i]})
	self.vintention, self.dintention = evaluate(self.intention, dists, value, cnode)

	// Deepsearch
	var alternative = make([]*Node, len(best))
	var altVal, altDel int
	if rand.Float64() < self.deepsearch {
		for a := 0; a < len(best) - 1; a++ {
			for b := a + 1; b < len(best); b++ {
				alternative = append(append(current[:a], reverse(current[a:b])...), current[b:]...)
				altVal, altDel = evaluate(alternative, dists, value, cnode)
				if altVal + altDel < val + d {
					current, val, d = alternative, altVal, altDel
				}
			}
		}
	}

	// Eventually update pbest
	if val + d < self.vpbest + self.dpbest {
		self.pbest, self.vpbest, self.dpbest = current, val, d
	}

	return self.pbest, self.vpbest, self.dpbest
}
// *****************************************************************************************************************
//                                                      END SWARM
// *****************************************************************************************************************