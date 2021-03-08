package dei

// ---------------------------------- Algorithm Abstract ---------------------------------------
// ---------------------------------------------------------------------------------------------
type Algorithm interface {
	// Execute the algorithm on a subpath
	execute([]*Node, [][]int, int, *Node)
	// Get the solution found, its value, and the cumulated delay
	getSolution() (Solution, int, int)
}
// ---------------------------------------------------------------------------------------------