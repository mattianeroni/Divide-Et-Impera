"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In this package are collected the algorithms which might be incorported in the
DivideEtImpera (DEI) algorithm.

All these algorithms, to be incorporated in the DEI, must inherit from the
Algorithm abstract class provided in the file where the DEI is written too.
Furthermore, at least the best solution must be a data structure as that one
handled by the DEI (see Solution class), and the nodes must be data structures
similar to those used by the DEI (see Node class).


Written by Mattia Neroni in July 2020.

Author contact: mattia.neroni@unipr.it

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
from .shuffler import Shuffler
from .randomsearch import RandomSearch
from .twoopt import TwoOpt
from .greedy import Greedy
from .biasedrandomised import BiasedRandomised
from .hybrid_tabu_annealing import HybridTabuAnnealing
from .pso import ParticleSwarmOptimization
