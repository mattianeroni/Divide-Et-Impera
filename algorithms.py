from __future__ import annotations
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In this file are written the algorithms which might be incorported in the
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





"""
Libraries imported from Python 3 standard library.
"""
import random
import copy
import math
import numpy # type: ignore
import itertools
import collections # type: ignore
import matplotlib.pyplot as plt # type: ignore

from typing import Tuple, Dict, List, Optional, cast, Deque, Callable


"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node, cost












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
        current_path = random.sample(tour, len(tour))
        best = self.evaluate (tuple(current_path), current_value, current_node, distances)
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
        tour = tuple(random.sample(tour, len(tour)))
        builder = Greedy(self.alpha, self.starting_beta)
        best = self.evaluate (tour, current_value, current_node, distances)

        for i in range (self.iter):
            builder.exe (current_value, tour, current_node, distances)
            new_sol = builder.get_best_solution

            if cost(new_sol) < cost(best):
                best = new_sol
                builder.beta = self.starting_beta
            else:
                builder.beta = min(1.0, builder.beta + self.delta_beta)

        self.set_best_solution (best)






class HybridTabuAnnealing (Algorithm):
    """
    An instance of this class represents the algorithm published by Ilker Küçüko,
    Reginald Dewil and Dirk Cattrysse, entitled 'Hybrid simulated annealing and tabu
    search method for the electric travelling salesman problem with time windows and
    mixed charging rates'.

    """
    def __init__ (self,
                  era : int = 1000,
                  cooling : float = 0.95,
                  perturbation : float = 0.1,
                  perturbed : float = 0.1,
                  tabusize : int = 400):
        """
        Initialize.

        :param era: The number of iterations.
        :param cooling: The cooling of temperature at each iteration.
        :param perturbation: The perturbation probability.
        :param perturbed: The number of nodes perturber at each perturbation.
        :param tabusize: The size of the tabu list.

        """
        self.era = era
        self.cooling = cooling
        self.perturbation = perturbation
        self.perturbed = perturbed
        self.tabusize = tabusize

        self.t : float = 500.0
        self.tabu : Deque[Tuple[str, Node, Node]] = collections.deque(())



    def shiftleft(self, tour : Tuple[Node,...], dists : Dict[int,Dict[int,int]], details : Tuple[Tuple[Node,...], Tuple[Node,...]]) -> List[Node]:
        """
        One shift left operation.

        """
        waits, delays = details

        if len(delays) > 0:
            other = tour[random.randint(0, max(tour.index(moved := random.choice(delays))-1,0))]
            counter = 0
            while (op := ("shiftleft", other, moved) ) in self.tabu and (counter := counter + 1) < 1000:   # or dists[moved.id][other.id] != -1:
                other = tour[random.randint(0, max(tour.index(moved := random.choice(delays))-1,0))]

            if len(self.tabu) == self.tabusize:
                self.tabu.popleft()
            self.tabu.append(op)

            newtour : List[Node] = list(tour)
            i1, i2 = newtour.index(other), newtour.index(moved)
            newtour.pop(i2)
            newtour.insert (i1, moved)

        return newtour or list(tour)





    def shiftright (self, tour : Tuple[Node,...], dists : Dict[int,Dict[int,int]], details : Tuple[Tuple[Node,...], Tuple[Node,...]]) -> List[Node]:
        """
        One shift right operation.

        """
        waits, delays = details

        if len(waits) > 0:
            other = tour[random.randint(tour.index(moved := random.choice(waits)), len(tour)-1)]
            counter = 0
            while (op := ("shiftright", other, moved) ) in self.tabu and (counter := counter + 1) < 1000: # or dists[moved.id][other.id] != -1:
                other = tour[random.randint(tour.index(moved := random.choice(waits)), len(tour)-1)]


            if len(self.tabu) == self.tabusize:
                self.tabu.popleft()
            self.tabu.append(op)

            newtour : List[Node] = list(tour)
            i1, i2 = newtour.index(moved), newtour.index(other)
            newtour.pop(i1)
            newtour.insert (i2, moved)

        return newtour or list(tour)





    def opt (self, tour : Tuple[Node,...], dists : Dict[int,Dict[int,int]], details : Tuple[Tuple[Node,...], Tuple[Node,...]]) -> List[Node]:
        """
        2-OPT operation.

        """
        while (op := ("opt", random.choice(tour), random.choice(tour)) ) in self.tabu: # or dists[op[1].id][op[2].id] != -1:
            continue

        if len(self.tabu) == self.tabusize:
            self.tabu.popleft()
        self.tabu.append(op)

        newtour = list(tour)
        i1, i2 = newtour.index(op[1]), newtour.index(op[2])

        return newtour[:min(i1, i2)] + list(reversed(newtour[min(i1, i2):max(i1, i2)])) + newtour[max(i1, i2):]




    def swap (self, tour : Tuple[Node,...], dists : Dict[int,Dict[int,int]], details : Tuple[Tuple[Node,...], Tuple[Node,...]]) -> List[Node]:
        """
        2-OPT operation.

        """
        while (op := ("swap", random.choice(tour), random.choice(tour)) ) in self.tabu: # or dists[op[1].id][op[2].id] != -1:
            continue

        if len(self.tabu) == self.tabusize:
            self.tabu.popleft()
        self.tabu.append(op)

        newtour : List[Node] = list(tour)
        i1, i2 = newtour.index(op[1]), newtour.index(op[2])
        newtour[i1] = op[2]; newtour[i2] = op[1]

        return newtour





    def localsearch (self,
                     tour : Tuple[Node,...],
                     current_value : int,
                     current_node : Node,
                     distances : Dict[int,Dict[int,int]],
                     dists : Dict[int,Dict[int,int]],
                     details : Tuple[Tuple[Node,...],Tuple[Node,...]]
                    ) -> Solution:
        """
        Generation of another solution in the neighbourhood.

        """
        func : Callable = random.choice((self.shiftleft, self.shiftright, self.opt, self.swap))
        newtour : List[Node] = func(tour, dists, details)

        # Eventual perturbation
        if (r := random.random()) < self.perturbation:
            for _ in range(int(len(newtour) * self.perturbed)):
                removed_node = newtour.pop(random.randint(0, len(newtour) - 1))
                newtour.insert(random.randint(0, len(newtour) - 1), removed_node)

        return self.evaluate(tuple(newtour), current_value, current_node, distances)



    def get_details(self, solution : Solution, current_value : int, current_node : Node, distances : Dict[int, Dict[int,int]]) -> Tuple[Tuple[Node,...],Tuple[Node,...]]:
        waits, delays = [], []
        value, delay, cnode = current_value, 0, current_node
        for node in solution.result:
            if node.open - value + distances[cnode.id][node.id] > 0:
                waits.append(node)
            value = max(node.open, value + distances[cnode.id][node.id])

            if value - node.close > 0:
                delays.append(node)
            delay += max(0, value - node.close)
            cnode = node

        return tuple(waits), tuple(delays)






    def exe (self, current_value : int, tour : Tuple[Node,...], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:

        # Preprocessing
        dists = copy.deepcopy(distances)
        for n1, n2 in itertools.product(tour, tour, repeat=1):
            if n1 is not n2:
                if n1.open + distances[n1.id][n2.id] > n2.close:
                    dists[n1.id][n2.id] = -1

        # Sort nodes by ascending closing time
        sorted_tour : List[Node] = sorted(tour, key=lambda i: i.close)

        # Starting solution
        x = self.evaluate(tuple(sorted_tour), current_value, current_node, distances)

        waits, delays = self.get_details(x, current_value, current_node, distances)


        # Make sure the starting solution is feasible with no delay
        #counter = 0
        while x.delay > 0:
            x_new = self.localsearch (tuple(x.result), current_value, current_node, distances, dists, (waits, delays))
            if x_new.delay < x.delay:
                x = x_new
                waits, delays = self.get_details(x, current_value, current_node, distances)
            """
            else:
                counter += 1
                if counter > 100:
                    print("shuffle")
                    counter = 0
                    tour = random.sample(tour, len(tour))
                    x = self.evaluate(tuple(tour), current_value, current_node, distances)
                    waits, delays = self.get_details(x, current_value, current_node, distances)"""
        print("made feasible")

        for _ in range (self.era):

            # New solution in the neighbourhood
            x_new = self.localsearch (tuple(x.result), current_value, current_node, distances, dists, (waits, delays))

            # Eventually update the best
            r = random.random()
            if (i := cost(x_new)) < (j := cost(x)) or r > math.exp(- (i-j) / self.t):
                x = x_new
                waits, delays = self.get_details(x, current_value, current_node, distances)


            # Update the temperature
            self.t *= 0.9
            print(x.value, x.delay)


        self.set_best_solution(x)
