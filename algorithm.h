#ifndef EIG_ALGORITHM_H
#define EIG_ALGORITHM_H

#include "node.h"
#include <vector>
#include <array>

using std::vector;
using std::array;

// Template the number of nodes
template <std::size_t N>


class Algorithm {
    /*

     This is an abstract class.
     From this class should inherit all the algorithms that
     want to be included in the Divide-Et-Impera.

     */

protected:
    long cost;              // The cost of the best solution found
    vector<Node> best;      // The best solution found so far

    // Set the best solution and its cost
    virtual void set_best (vector<Node>, long cost);
    
    // Get the cost of a solution
    virtual long costify (vector<Node>, array<array<Node,N>,N>);
};


void Algorithm<N>::set_best (vector<Node> sol, long cost) {// array<array<long,N>,N> dists) {
    (*this).best = sol; (*this).cost = cost;
}

template<std::size_t N>
long Algorithm<N>::costify (vector<Node> sol, array<array<long,N>,N> dists) {
    long cost = 0;
    for (int i = 0; i < sol.size() - 1; ++i)
        cost += dists[sol[i]][sol[i+1]];
    return cost;
}

#endif //EIG_ALGORITHM_H
