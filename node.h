#ifndef EIG_NODE_H
#define EIG_NODE_H


#include <math.h>



struct Node {
    /*

    An instance of this class represents a node of the graph.

    */


    int id, x, y, open, close;            // Id, x-position, y-position, opening time, closing time

    Node (int,int,int,int,int);           // Constructor
    ~Node();                              // Destructor

    int operator-(const Node&) const;     // Distance between two nodes is calculated with this operator

};


// Constructor
Node::Node (int id, int x, int y, int open, int close) : id(id), x(x), y(y), open(open), close(close){}

// Destructor
Node::~Node(){}


// Euclidean distance with another node
int Node::operator-(const Node& other) const {
    return (int) pow(pow(x - other.x, 2) + pow(y - other.y, 2), 0.5);
}



#endif //EIG_NODE_H