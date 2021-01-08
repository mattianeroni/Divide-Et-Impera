#include <iostream>
#include <vector>
#include <string>
#include <random>

#include "utils.h"
#include "dei.h"
#include "greedy.h"
#include "bra.h"

using namespace std;

vector<string> files = {"n200w100.001.txt",  "n250w100.001.txt",  "n300w100.001.txt",  "n400w100.001.txt",
                        "n200w100.002.txt",  "n250w100.002.txt",  "n300w100.002.txt",  "n400w100.002.txt",
                        "n200w100.003.txt",  "n250w100.003.txt",  "n350w100.003.txt",  "n400w100.003.txt",
                        "n200w100.004.txt",  "n250w100.004.txt",  "n350w100.004.txt",  "n400w100.004.txt",
                        "n200w100.005.txt",  "n250w100.005.txt",  "n350w100.005.txt",  "n400w100.005.txt",
                        "n200w200.001.txt",  "n250w200.001.txt",  "n350w200.001.txt",  "n400w200.001.txt",
                        "n200w200.002.txt",  "n250w200.002.txt",  "n350w200.002.txt",  "n400w200.002.txt",
                        "n200w200.003.txt",  "n250w200.003.txt",  "n350w200.003.txt",  "n400w200.003.txt",
                        "n200w200.004.txt",  "n250w200.004.txt",  "n350w200.004.txt",  "n400w200.004.txt",
                        "n200w200.005.txt",  "n250w200.005.txt",  "n350w200.005.txt",  "n400w200.005.txt",
                        "n200w300.001.txt",  "n250w300.001.txt",  "n350w300.001.txt",  "n400w300.001.txt",
                        "n200w300.002.txt",  "n250w300.002.txt",  "n350w300.002.txt",  "n400w300.002.txt",
                        "n200w300.003.txt",  "n250w300.003.txt",  "n350w300.003.txt",  "n400w300.003.txt",
                        "n200w300.004.txt",  "n250w300.004.txt",  "n350w300.004.txt",  "n400w300.004.txt",
                        "n200w300.005.txt",  "n250w300.005.txt",  "n350w300.005.txt",  "n400w300.005.txt",
                        "n200w400.001.txt",  "n250w400.001.txt",  "n350w400.001.txt",  "n400w400.001.txt",
                        "n200w400.002.txt",  "n250w400.002.txt",  "n350w400.002.txt",  "n400w400.002.txt",
                        "n200w400.003.txt",  "n250w400.003.txt",  "n350w400.003.txt",  "n400w400.003.txt",
                        "n200w400.004.txt",  "n250w400.004.txt",  "n350w400.004.txt",  "n400w400.004.txt",
                        "n200w400.005.txt",  "n250w400.005.txt",  "n350w400.005.txt",  "n400w400.005.txt",
                        "n200w500.001.txt",  "n250w500.001.txt",  "n350w500.001.txt",  "n400w500.001.txt",
                        "n200w500.002.txt",  "n250w500.002.txt",  "n350w500.002.txt",  "n400w500.002.txt",
                        "n200w500.003.txt",  "n250w500.003.txt",  "n350w500.003.txt",  "n400w500.003.txt",
                        "n200w500.004.txt",  "n250w500.004.txt",  "n350w500.004.txt",  "n400w500.004.txt",
                        "n200w500.005.txt",  "n250w500.005.txt",  "n350w500.005.txt",  "n400w500.005.txt"};


void experiment() {


    for (auto filename : files) {
        auto nodes = read_file(filename);
        auto dists = build_dists(nodes);

        auto bra = new BRA();

        auto dei = DEI(bra, dists, &nodes[0], 50, 3000);
        dei(nodes);
        cout << "yo\n";
        cout << dei.value << " " << dei.delay << endl;
        delete bra;



    }
}




int main ()
{
    srand(time(NULL));
    experiment();
    cout << "Program concluded.";
    return 0;
    
    
}
