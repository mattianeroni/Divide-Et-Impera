from __future__ import annotations
"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Node


"""
Libraries imported from Python 3 standard library.
"""
import random
from typing import Tuple, Dict





class Shuffler (Algorithm):

    """
    This algorithm randomly shuffle the nodes to visit, by generating in this way
    a random tour.
    After that, the cost of the solution is calculated.

    """



    def __init__ (self) -> None:
        """
        Initialize.
        """
        super().__init__()





    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method of the algorithm.

        """
        random.shuffle (list(tour))
        self.set_best_solution (self.evaluate (tuple(tour), current_value, current_node, distances))
