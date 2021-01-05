#ifndef UNTITLED_GREEDY_H
#define UNTITLED_GREEDY_H

#define self (*this)

#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include "node.h"


using std::log;
using std::max;


template<std::size_t N>

class Greedy : protected Algorithm<N>{

private:

    float alpha, beta;

    Greedy(float, float);
    ~Greedy() = default;

    void exe (const Node&, long, vector<Node>, array<array<Node,N>,N>);
    int bra (int);

};


template<std::size_t N>
Greedy<N>::Greedy(float alpha, float beta) : alpha(alpha), beta(beta){}

template<std::size_t N>
int Greedy<N>::bra (int length){
    return (int) (log( rand() / (float) RAND_MAX ) / log(1 - alpha)) % length;
}

template<std::size_t N>
void Greedy<N>::exe(const Node& cnode, long cval, vector<Node> tour, array<array<Node,N>,N> dists){
    int stay_equal = (int) beta * tour.size();
    vector<Node> sol(tour.begin(), tour.begin() + stay_equal);
    vector<Node> options(tour.begin() + stay_equal, tour.end());

    while (!options.empty()){
        std::sort(options.begin(), options.end(),
                  [cnode, cval, dists](const Node& n, const Node& m) -> bool
                  {
                    return max(dists[cnode.id][n.id] + cval, n.open) - max(0, dists[cnode.id][n.id] + cval - n.close)
                    < max(dists[cnode.id][m.id] + cval, m.open) - max(0, dists[cnode.id][m.id] + cval - m.close);
                  }
        );
        int id = bra(options.size());
        sol.push_back(options[id]);
        options.erase(options.begin() + id);
    }

    auto cost = self.costify(cnode, cval, sol, dists);
    self.set_best(sol, cost);
}



#endif //UNTITLED_GREEDY_H
