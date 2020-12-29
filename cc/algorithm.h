#ifndef EIG_ALGORITHM_H
#define EIG_ALGORITHM_H

#include "node.h"
#include <vector>
#include <array>
#include <cmath>

using std::vector;
using std::array;
using std::pair;

// Template the number of nodes
template <std::size_t N>


class Algorithm {
    /*

     This is an abstract class.
     From this class should inherit all the algorithms that
     want to be included in the Divide-Et-Impera.

     */

protected:
    long value, delay;      // The travel time relative to the best solution found and
                            // the cumulated delay
    vector<Node> best;      // The best solution found so far

    // Set the best solution and its cost
    void set_best (vector<Node>, pair<long,long> cost);
    
    // Get the cost of a solution
    pair<long,long> costify (const Node&, long, vector<Node>, array<array<Node,N>,N>);

    // The execution abstract method
    virtual void exe (const Node&, long, vector<Node>, array<array<Node,N>,N>);

};


template<std::size_t N>
void Algorithm<N>::set_best (vector<Node> sol, pair<long,long> cost) {
    (*this).best = sol; (*this).value = cost.first; (*this).delay = cost.second;
}


template<std::size_t N>
pair<long,long> Algorithm<N>::costify(const Node& cnode, long cval, vector<Node> sol, array<array<Node, N>, N> dists) {
    Node current = cnode; long val = cval, del = 0;
    for (auto n : sol){
        val = std::max (n.open, val + dists[current.id][n.id]);
        del += std::max((long) 0, val - n.close);
        current = n;
    }
    return pair<long,long> (val, del);
}

#endif //EIG_ALGORITHM_H
