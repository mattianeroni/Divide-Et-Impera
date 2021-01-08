#ifndef UNTITLED_GREEDY_H
#define UNTITLED_GREEDY_H

#define self (*this)

#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include "node.h"


using std::vector;
using std::log;
using std::max;




class Greedy : public Algorithm{

public:

    float alpha, beta;

    int bra (int) const ;
    void exe (const Node&, long, vector<Node>, vector<vector<int>>) override;

    explicit Greedy(float=0.9999, float=1.0);
    ~Greedy() = default;

};


Greedy::Greedy(float alpha, float beta) : alpha(alpha), beta(beta){}


int Greedy::bra (int length) const {
    return (int) (log( rand() / (float) RAND_MAX ) / log(1 - alpha)) % length;
}


void Greedy::exe(const Node& cnode, long cval, vector<Node> tour, vector<vector<int>> dists){
    int stay_equal = (int) (beta * tour.size());
    vector<Node> sol(tour.begin(), tour.begin() + stay_equal);
    vector<Node> options(tour.begin() + stay_equal, tour.end());

    while (!options.empty()){
        std::sort(options.begin(), options.end(),
                  [cnode, cval, dists](const Node& n, const Node& m) -> bool
                  {
                    return max(dists[cnode.id][n.id] + cval, (long)n.open) - max((long)0, dists[cnode.id][n.id] + cval - n.close)
                    < max(dists[cnode.id][m.id] + cval, (long) m.open) - max((long)0, dists[cnode.id][m.id] + cval - m.close);
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
