from __future__ import annotations
"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Node, cost, Solution


"""
Libraries imported from Python 3 standard library.
"""
import random
from typing import Tuple, Dict, List






class TwoOpt (Algorithm):
    """
    This is the 2-OPT algorithm. At each iteration, all the possible combinations
    of cutting points are tried by iterating the tour from the beginning until the
    end. Each time a better solution is found the best is updated.

    Thus, given I the number of iterations, and L the length of the tour, the
    number of possible solutions explored is I * L * (L - 1) / 2.

    Moreover, if the parameter <deep> is True, the research of a better solution
    is even more thorough, and, every time a better solution if found, the algorithm
    restarts trying the cutting points from the beginning of the tour, before
    starting the next iteration.

    """

    def __init__ (self):
        """
        Initialize.

        """
        super().__init__()





    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This method is the execution of the algorithm. Please refer to the
        beginning of the class for a more accurate description of the
        procedure.

        """
        current_path : List[Node] = random.sample(tour, len(tour))
        best : Solution = self.evaluate (tuple(current_path), current_value, current_node, distances)
        i = 0
        while i < len(tour) - 2:
            j = i + 2
            while j < len(tour):
                new_sol = self.evaluate(tuple(current_path[:i] + list(reversed(current_path[i:j])) + current_path[j:]), current_value, current_node, distances)
                j += 1
                if cost(new_sol) < cost(best):
                    best = new_sol
                    i, j = 0, 2
            i += 1

        self.set_best_solution (best)
