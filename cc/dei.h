#ifndef UNTITLED_DEI_H
#define UNTITLED_DEI_H


#define self (*this)

#include <vector>
#include <array>
#include "node.h"
#include "algorithm.h"

template<typename T>

using vec = std::vector<T>;
using std::array;




// Template the number of nodes
template <std::size_t N>




class DEI{

private:

    Algorithm<N>*              alg;

    array<array<long,N>,N>  dists;
    Node*                   cnode;
    vec<Node>               solution;
    long                    value, delay;
    int                     p, maxsplit;

    void solve(vec<Node>);

public:

    DEI(Algorithm<N>*, array<array<long,N>,N>, Node*, int = 50, int = 3000);
    ~DEI() = default;
    void operator()(vec<Node>);

};


// Constructor
template <std::size_t N>
DEI<N>::DEI(Algorithm<N>* alg, array<array<long,N>,N> dists, Node* cnode, int p, int maxsplit) : alg(alg),
                    dists(dists), cnode(cnode), value(0), delay(0), p(p), maxsplit(maxsplit){}


template <std::size_t N>
void DEI<N>::operator()(vec<Node> tour){
    if (tour.size() > p){
        vec<Node> f, s; int split = 0;
        while ((f.size() == 0 || s.size() == 0) && split++ < maxsplit){
            auto pivot = tour[rand() % tour.size()];
            for (auto n : tour)
                if (n.close < pivot.open){
                    f.push_back(n);
                } else {
                    s.push_back(n);
                }
        }

        if (f.size() == 0 || s.size() == 0){
            solve(tour);
        } else {
            self(f); self(s);
        }

    } else {
        solve(tour);
    }
}



template <std::size_t N>
void DEI<N>::solve (vec<Node> sol){
    // Solve the subsolution with the implemented algorithm
    alg->exe(*cnode, value, sol, dists);

    // Update the solution, its travel time and its delay
    solution.insert(solution.end(), alg->best.begin(), alg->best.end());
    value = alg->value; delay += alg->delay;
}
#endif //UNTITLED_DEI_H
