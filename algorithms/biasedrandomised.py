from __future__ import annotations


"""
Import from Python3 Standard library.
"""
import random
from typing import Tuple, Dict


"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node, cost
from .greedy import Greedy



class BiasedRandomised (Algorithm):
    """
    This algorithms is the implementation of a Biased Randomised mataheuristic framework.

    At each iteration of the algorithm a new solution is constructed. The new solution
    is therefore compared to the current best, and, if better, it is made the new best.

    The parameter <alpha>, according to a quasi-geometric distribution, define
    the greedyness of the algorithm and the probability to select at each step
    the best option. Before constructing a new solution, all nodes are sorted from
    the best to the worst. Then, to each node is assigned a probability to be selected
    according to its position in the list using a quasi-geometric function:

                        f(x) = (1 - alpha)^x

    Hence, a node is selected and made the current one, and the process is repeated
    until the new solution has not been constructed.
    The classification of the nodes is made according to the following function. Given
    i the current node (i.e. the last seleted node) and j a generic node that can be
    selected next, we define Dij the distance-in-time between the two nodes, Ti the
    current time (i.e. the current value of the solution in construction), Sj the
    opening time of the node j, and Cj the closing time of the node j.
    The 'cost' of the node j is caculated considering the travel-time, the eventual
    waiting time in case j in reached before its opening time, and the delay in case j
    is reached after its closing time. Hence, the cost of j Qj is:

              Qj = Dij + max{0, Sj - (Ti + Dij)} + max{0, Ti + Dij - Cj}

    """



    def __init__ (self, alpha : float = 0.9, starting_beta : float = 0.1, delta_beta : float = 0.1, iter : int = 3000) -> None:
        """
        Initialize.

        :param alpha: The parameter of the quasi-geometric function f(x) = (1 - alpha)^x
        :param iter: The number of solutions explored.

        """
        super().__init__()

        self.alpha = alpha
        self.starting_beta = starting_beta
        self.delta_beta = delta_beta
        self.iter = iter





    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.

        Until the number of iterations defined is not elapsed a new solution
        is constructed via Biased Randomised Algorithm.
        At the end of the process, only the best solution found so far is kept.

        """
        tour2 : Tuple[Node,...] = tuple(random.sample(tour, len(tour)))
        builder = Greedy(self.alpha, self.starting_beta)
        best : Solution = self.evaluate (tour2, current_value, current_node, distances)

        for i in range (self.iter):
            builder.exe (current_value, tour2, current_node, distances)
            new_sol = builder.get_best_solution

            if cost(new_sol) < cost(best):
                best = new_sol
                builder.beta = self.starting_beta
            else:
                builder.beta = min(1.0, builder.beta + self.delta_beta)

        self.set_best_solution (best)
