#ifndef UNTITLED_DEI_H
#define UNTITLED_DEI_H


#define self (*this)

#include <vector>
#include <array>
#include "node.h"
#include "algorithm.h"
#include "greedy.h"

template<typename T>
using vec = std::vector<T>;
using std::array;



class DEI{

private:

    Algorithm*              alg;

    vector<vector<int>>     dists;
    Node*                   cnode;

    void solve(vec<Node>);

public:

    vec<Node>               solution;
    long                    value, delay;
    int                     p, maxsplit;

    DEI(Algorithm*, vector<vector<int>>, Node*, int = 50, int = 3000);
    ~DEI() = default;
    void operator()(vec<Node>);

};


// Constructor
DEI::DEI(Algorithm* alg, vector<vector<int>> dists, Node* cnode, int p, int maxsplit) : alg(alg),
                    dists(dists), cnode(cnode), value(0), delay(0), p(p), maxsplit(maxsplit){}



void DEI::operator()(vec<Node> tour){
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



void DEI::solve (vec<Node> sol){
    std::cout << "yu\n";
    // Solve the subsolution with the implemented algorithm
    alg->exe(*cnode, value, sol, dists);
    std::cout << "here\n";
    // Update the solution, its travel time and its delay
    solution.insert(solution.end(), alg->best.begin(), alg->best.end());
    value = alg->value; delay += alg->delay;
}
#endif //UNTITLED_DEI_H
