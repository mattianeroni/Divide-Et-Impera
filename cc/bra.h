#ifndef UNTITLED_BRA_H
#define UNTITLED_BRA_H

#define self (*this)

#include <vector>
#include "node.h"



class BRA : public Algorithm {

public:

    float alpha, betastart, betaend, betastep;
    int maxiter;

private:
    void exe (const Node&, long, vector<Node>, vector<vector<int>>);

public:
    BRA(float = 0.9, float = 0.1, float = 0.9, float = 0.1, int = 1000);
    ~BRA() = default;
};


BRA::BRA(float alpha, float betastart, float betaend, float betastep, int maxiter) :
alpha(alpha), betastart(betastart), betaend(betaend), betastep(betastep), maxiter(maxiter){}


void BRA::exe (const Node& cnode, long cval, vector<Node> tour, vector<vector<int>> dists){
    auto builder = new Greedy(alpha, betastart);
    vector<Node> bestsol; pair<long,long> bcost;

    for (int i = 0; i  < maxiter; ++i){
        std::cout << "yOoo\n";
        builder->exe(cnode, cval, tour, dists);
        std::cout << "ya\n";
        if (builder->value + builder->delay < bcost.first + bcost.second){
            bestsol = builder->best;
            bcost = pair<long,long>(builder->value, builder->delay);
            builder->beta = betastart;
        } else {
            builder->beta = std::max(builder->beta + betastep, betaend);
        }
    }
    delete builder;
    set_best(best, bcost);

}

#endif //UNTITLED_BRA_H
