package dei

import "math"

// A node of the Graph
type Node struct {
	id, x, y, open, close int
}


// Constructor
func NewNode (id, x, y, open, close int ) *Node {
	return &Node{id, x, y, open, close}
}


// The cost of a node given a specific situation
func (self *Node) Cost (cnode Node, dists [][]int, value int) int {
	var d int = dists[cnode.id][self.id]
	return int(math.Max(float64(self.open), float64(value + d)) - math.Max(0, float64(value + d - self.close)))
}


// Euclidean distance between two nodes
func Euclidean (n, m Node) int {
	return int(math.Sqrt(math.Pow(float64(n.x - m.x), 2.0) + math.Pow(float64(n.y - m.y), 2.0)))
}
