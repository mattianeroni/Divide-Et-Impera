#include <iostream>
#include "utils.h"
#include "algorithm.h"
#include "dei.h"
#include "greedy.h"

using namespace std;
using namespace utils;

int main() {
    srand (time(NULL));

    //auto v = read_file("n200w100.001.txt");

    for (int i = 0; i < 1000; ++i)
        cout << (int) (log( (float) rand() / RAND_MAX ) / log(1 - 0.4)) % 20 << endl;

    cout << "Program concluded.";
    return 0;
}
