#ifndef EIG_UTILS_H
#define EIG_UTILS_H

#include <array>
#include "node.h"

using std::array;


namespace utils {
    // Template the number of nodes
    template<std::size_t N>


    array<array<long,N>,N> build_dists (array<Node,N> arr){
        array<array<long,N>,N> res;
        for (const Node& n : arr)
            for (const Node& m : arr)
                res[n.id][m.id] = n - m;
        return res;    
    }
}


#endif //EIG_UTILS_H
