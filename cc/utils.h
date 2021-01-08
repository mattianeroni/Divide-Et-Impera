#ifndef EIG_UTILS_H
#define EIG_UTILS_H

#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "node.h"

using std::vector;
using std::string;
using std::fstream;

template <typename T>
using matrix = vector<vector<T>>;

template <typename T>
using matrix = vector<vector<T>>;

namespace std {



    // This method takes a string and split it in tokens
    vector<string> tokenize(string row, string delim = " ") {
            vector<string> output; string substring;

            string::size_type prev_pos = 0, pos = 0;

            while((pos = row.find(delim, pos)) != string::npos)
            {
                substring = row.substr(prev_pos, pos-prev_pos);
                if (substring != "")
                    output.push_back(substring);
                prev_pos = ++pos;
            }
            substring = row.substr(prev_pos, pos-prev_pos);
            if (substring != "")
                output.push_back(substring); // Last word

            return output;
    }





    vector<Node> read_file (string name, string path = "../benchmarks/"){
        vector<Node> v; fstream file; string row; vector<string> tokens; int i = 0;

        file.open(path.append(name));
        if (!file)
            throw "File not found.";

        while (getline(file, row)){
            if (i > 0){
                tokens = tokenize(row);
                v.push_back(Node(stoi(tokens[0]) - 1,
                                     (int) stof(tokens[1]),
                                     (int) stof(tokens[2]),
                                     (int) stof(tokens[4]),
                                     (int) stof(tokens[5]))
                        );
            }
            ++i;
        }
        return v;
    }


    matrix<int> build_dists (vector<Node> arr){
        matrix<int> res(arr.size(), vector<int>(arr.size(),0));
        for (const Node& n : arr)
            for (const Node& m : arr)
                res[n.id][m.id] = n - m;

        return res;    
    }
}


#endif //EIG_UTILS_H
