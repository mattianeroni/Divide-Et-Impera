#ifndef DEI_DEI_H
#define DEI_DEI_H

#include <array>
#include <vector>

#include "node.h"
#include "algorithm.h"

#define self (*this)

using std::array;
using std::vector;


// Template the number of nodes
template<std::size_t N>



struct DivideEtImpera {

    array<array<long,N>,N> dists;                           // The distance matrix
    vector<Node> solution;                                  // The current solution
    Node& cnode;                                            // The current node
    long value, delay;                                      // The travel time and the cumulative delay of the
                                                            // current solution.
    Algorithm<N>* alg;                                      // The implemented algorithm
    int p, maxsplit;                                        // Parameters of the algorithm

    DivideEtImpera(Algorithm<N>*, array<array<long,N>,N>, const Node&, int=50, int=3000);  // Constructor
    ~DivideEtImpera() = default;                            // Destructor

    void operator()(vector<Node>);                          // The eecution of the algorithm

    void solve(vector<Node>);                               // Solve a subtour using the implemented algorithm
};


template<std::size_t N>
DivideEtImpera<N>::DivideEtImpera(Algorithm<N>* alg, array<array<long,N>,N> dists, const Node& cnode, int p, int maxsplit)
: alg(alg), dists(dists), value(0), delay(0), p(p), maxsplit(maxsplit), cnode(cnode) {}


template<std::size_t N>
void DivideEtImpera<N>::operator()(vector<Node> tour){
    tour.erase(std::find(tour.begin(), tour.end(), cnode));
    if (tour.size() > p) {
        vector<Node> f, s;
        int split = 0;


        while ((f.size() == 0 || s.size() == 0) && split++ < maxsplit){
            auto pivot = tour[(int) ((float) rand() / RAND_MAX * tour.size())];
            for (Node n : tour){
                if (n.close < pivot.open){
                    f.push_back(n);
                } else{
                    s.push_back(n);
                }
            }
        }

        if (f.size() > 0 && s.size() > 0){
            (*this)(f); (*this)(s);
        }else{
            solve(tour);
        }


    } else {
        solve(tour);
    }
}


template<std::size_t N>
void DivideEtImpera<N>::solve(vector<Node> tour){
    alg->exe(cnode, value, tour, dists);
    self.solution.insert(self.solution.end(),alg->best.begin(),alg->best.end());
    self.value = alg->value; self.delay += alg->delay;
}






















#endif //DEI_DEI_H
