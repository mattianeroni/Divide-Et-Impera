#ifndef EIG_ALGORITHM_H
#define EIG_ALGORITHM_H

#define self (*this)

#include "node.h"
#include <vector>
#include <array>
#include <cmath>

using std::vector;
using std::array;
using std::pair;
using std::max;

// Template the number of nodes
template <std::size_t N>


class Algorithm {
    /*

     This is an abstract class.
     From this class should inherit all the algorithms that
     want to be included in the Divide-Et-Impera.

     */

protected:
    long value, delay;       // The travel time and the cumulated delay relative to the best solution found
    vector<Node> best;      // The best solution found so far

    // Set the best solution and its cost
    void set_best (vector<Node>, pair<long, long> cost);
    
    // Get the cost of a solution
    // (current node, current val, tour, dists)
    pair<long, long> costify (const Node&, long, vector<Node>, array<array<Node,N>,N>);


    // Execution of the implemented algorithm
    // (current node, current val, tour, dists)
    virtual void exe (const Node&, long, vector<Node>, array<array<Node,N>,N>);

};

template <std::size_t N>
void Algorithm<N>::set_best (vector<Node> sol, pair<long, long> cost) {
    self.best = sol; self.value = cost.first; self.delay = cost.second;
}


template<std::size_t N>
pair<long, long> Algorithm<N>::costify(const Node & cnode, long cval, vector<Node> sol, array<array<Node, N>, N> dists) {
    long val = cval, del = 0;
    Node c = cnode;
    for (Node i : sol) {
        val = max(i.open, val + dists[cnode.id][i.id]);
        del += max((long) 0, val - i.close);
    }
    return pair(val, del);
}

#endif //EIG_ALGORITHM_H
