from __future__ import annotations
"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Node, cost
from .shuffler import Shuffler

"""
Libraries imported from Python 3 standard library.
"""
import random
from typing import Tuple, Dict



class RandomSearch (Algorithm):

    """
    This algorithm randomly shuffle the nodes to visit more and more times, by
    generating in this way more random tours.
    At each iteration, the algorithm keeps track of the best solution found
    so far.
    Finally, the best solution found is returned.

    """



    def __init__ (self, iter : int = 1000) -> None:
        """
        Initialize.

        :param iter: The number of iterations and solutions exlored
                     by the algorithm during its execution.

        """
        super().__init__()
        self.iter = iter





    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method of the algorithm. It inherits from the exe abstract
        method in the Algorithm abstract class.

        """
        s = Shuffler()
        best = self.evaluate (tuple(random.sample(tour, len(tour))), current_value, current_node, distances)

        for i in range(self.iter):
            s.exe (current_value, tour, current_node, distances)
            solution = s.get_best_solution

            if cost(solution) < cost(best):
                best = solution

        self.set_best_solution (best)
