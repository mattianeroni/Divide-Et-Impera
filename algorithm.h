#ifndef EIG_ALGORITHM_H
#define EIG_ALGORITHM_H

#include "node.h"
#include <array>

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
    array<Node, N> best;    // The best solution found so far

    // Set the best solution and its cost
    virtual void set_best (array<Node,N>, array<array<long,N>,N>);
};



template <std::size_t N>
void Algorithm<N>::set_best (array<Node,N> sol, array<array<long,N>,N> dists) {
    best = sol; cost = 0;
    for (int i = 0; i < sol.size() - 1; ++i)
        cost += dists[sol[i].id][sol[i+1].id];
}

#endif //EIG_ALGORITHM_H
