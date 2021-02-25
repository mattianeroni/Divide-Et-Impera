from __future__ import annotations
"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Node, Solution, cost

"""
Libraries imported from Python 3 standard library.
"""
import random
import math
from typing import Tuple, Dict, List








class Greedy (Algorithm):
    """
    This is the greedy algorithm with some additional characteristics.

    It is inspired by the Biased Randomised Algorithm, hence, there is an additional
    parameter <alpha>, which, according to a quasi-geometric distribution, define
    the greedyness of the algorithm and the probability to select at each step
    the best option.

    At each step of the algorithm, all the nodes that are not part of the current
    solution in construction yet, are sorted from the best to the worst.
    Then, to each node is assigned a probability to be selected according to its
    position in the list using a quasi-geometric function:

                        f(x) = (1 - alpha)^x

    At each step, the selectable nodes are classified defining which is the best
    and the worst. This evaluation is made according to the following function. Given
    i the current node (i.e. the last seleted node) and j a generic node that can be
    selected next, we define Dij the distance-in-time between the two nodes, Ti the
    current time (i.e. the current value of the solution in construction), Sj the
    opening time of the node j, and Cj the closing time of the node j.
    The 'cost' of the node j is caculated considering the travel-time, the eventual
    waiting time in case j in reached before its opening time, and the delay in case j
    is reached after its closing time. Hence, the cost of j Qj is:

              Qj = Dij + max{0, Sj - (Ti + Dij)} + max{0, Ti + Dij - Cj}

    """

    def __init__ (self, alpha : float = 0.999, beta : float = 1.0) -> None:
        """
        Initialize.

        :param alpha: The parameter of the quasi-geometric distribution.
                      Set alpha very close to 1 for a pure greedy behavior.

        :param beta: The percentage of the solution which is constructed from scratch.
                     The new solution can also be constructed just in part, but always
                     starting from the bottom.

        """
        super().__init__()

        self.alpha = alpha
        self.beta = beta




    @staticmethod
    def _costof (node : Node, current_node : Node, current_value : int, distances : Dict[int, Dict[int,int]]) -> int:
        """
        This is the cost method used to evaluate the nodes and define their probability
        to be selected. Obviously, only nodes not included yet in the current solution
        must be considered.

        """
        distance = distances[current_node.id][node.id]
        return max(node.open, current_value + distance) - max(0, current_value + distance - node.close)




    @staticmethod
    def _bra (lst : Tuple[Node,...], alpha : float) -> Node:
        """
        This method implements the biased randomisation by returning an
        element form a list, according to a quasi-geometric function.
                                f(x) = (1 - alpha)^x

        :param lst: the list of options
        :param alpha: the parameter of the quasi-geometric
        :return: the position in the list of the selected element

        """
        return lst[int(math.log (random.random(), 1 - alpha)) % len(lst)]





    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.

        Node-by-node, until the solution is not complete, a new node is selected according to
        the biased randomisation and included in the solution. Then, the value and the delay of
        the solution are updated, and the selected node is removed from the list of the
        future options.

        According to the parameter beta the tour can also be modified just in part, but always starting from the bottom.

        """
        rebuild_from : int = int(len(tour) * (1.0 - self.beta))

        current_tour : Tuple[Node, ...] = tour[:rebuild_from]
        solution : List[Node] = []
        value, delay = current_value, 0

        if len(current_tour) > 0:
            s = self.evaluate(current_tour, current_value, current_node, distances)
            solution, value, delay = list(s.result), s.value, s.delay

        current : Node = current_node if not current_tour else solution[-1]
        selectables : List[Node] = list(tour[rebuild_from:])

        while len(selectables) > 0:
            options = sorted(selectables, key=lambda n : self._costof (n, current, value, distances))
            next_node = self._bra(tuple(options), self.alpha)

            selectables.remove (next_node)
            solution.append (next_node)
            value += distances[current.id][next_node.id] + max(0, next_node.open - value - distances[current.id][next_node.id])
            delay += max(0, value - next_node.close)
            current = next_node

        self.set_best_solution (Solution(solution, value, delay))
