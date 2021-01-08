#ifndef EIG_ALGORITHM_H
#define EIG_ALGORITHM_H

#define self (*this)

#include "node.h"
#include <vector>
#include <cmath>

using std::vector;
using std::pair;
using std::max;



class Algorithm {

     // This is an abstract class.
     // From this class should inherit all the algorithms that
     // want to be included in the Divide-Et-Impera.

public:
    long value, delay;       // The travel time and the cumulated delay relative to the best solution found
    vector<Node> best;      // The best solution found so far

    // Set the best solution and its cost
    void set_best (vector<Node>, pair<long, long> cost);
    
    // Get the cost of a solution
    // (current node, current val, tour, dists)
    pair<long, long> costify (const Node&, long, vector<Node>, vector<vector<int>>);


    // Execution of the implemented algorithm
    // (current node, current val, tour, dists)
    virtual void exe (const Node&, long, vector<Node>, vector<vector<int>>) = 0;

    ~Algorithm() = default;

};



void Algorithm::set_best (vector<Node> sol, pair<long, long> cost) {
    self.best = sol; self.value = cost.first; self.delay = cost.second;
}



pair<long, long> Algorithm::costify(const Node& cnode, long cval, vector<Node> sol, vector<vector<int>> dists) {
    long val = cval, del = 0;
    Node c = cnode;
    for (Node i : sol) {
        val = max((long) i.open, val + dists[cnode.id][i.id]);
        del += max((long) 0, val - i.close);
    }
    return pair<long,long>(val, del);
}

#endif //EIG_ALGORITHM_H
