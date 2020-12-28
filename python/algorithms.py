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
from typing import Tuple, Sequence, List, Optional, Union, Dict, cast

import random
import copy
import math
import numpy # type: ignore
import matplotlib.pyplot as plt # type: ignore


"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node








def evaluate (tour : List[Node],
              current_value : int,
              current_node : Node,
              distances : Dict[int,Dict[int,int]]
             ) -> Solution:
    """
    This function can be used by all the algorithms implemented
    in this library to evaluate a solution, once the nodes to visit
    have been set in the desired order.
    Given the tour, the current value, and the current node, the function 
    returns a solution after calculating its value and delay.
    
    """
    solution : Solution = Solution(tour, current_value, 0)
    current : Node = current_node
    for node in tour:
        solution.value = max(node.readytime, solution.value + distances[current.id][node.id])
        solution.delay += max(0, solution.value - node.duedate) 
        current = node
    return solution
    
    
    
    
    





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





    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method of the algorithm.

        """

        random.shuffle (tour)
        solution : Solution = evaluate (tour, current_value, current_node, distances)
        self.set_best_solution (solution)











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





    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method of the algorithm. It inherits from the exe abstract
        method in the Algorithm abstract class.

        """
        s : Shuffler = Shuffler()
        best : Solution = evaluate (tour, current_value, current_node, distances)
        i : int = 0

        while i < self.iter:
            s.exe (current_value, tour, current_node, distances)
            solution : Solution = s.get_best_solution
            i += 1
            if best is None or solution.cost < best.cost:
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
    
    
    
    
    def __init__ (self, iter : int, deep : bool = False) -> None:
        """
        Initialize.
        
        :param iter: the number of iterations the algorithm is repeated
        :param deep: If this parameter is True, every time a better solution
                     is found, before going to the next iteration the algorithm
                     re-try all the couples of cutting points from the beginning
                     of the tour.
        
        """
        super().__init__()
        
        self.iter = iter
        self.deep = deep
        
        
        
        
        
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This method is the execution of the algorithm. Please refer to the 
        beginning of the class for a more accurate description of the 
        procedure.
        
        """
        best : Solution = evaluate (tour, current_value, current_node, distances)
            
        for _ in range(self.iter):
            i = 0
            while i < len(tour) - 1:
                j = i + 1
                while j < len(tour):
                    new_tour = tour[:i] + list(reversed(tour[i:j])) + tour[j:]
                    new_sol = evaluate (new_tour, current_value, current_node, distances)
                    j += 1
                    if new_sol.cost < best.cost:
                        best = new_sol
                        if self.deep:
                            i, j = 0, 1 
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
    
    def __init__ (self, alpha : float = 0.999, beta : float = 1.0):
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
    def _costof (node : Node, current_node : Node, current_value : int, distances : Dict[int,Dict[int,int]]) -> int:
        """
        This is the cost method used to evaluate the nodes and define their probability
        to be selected. Obviously, only nodes not included yet in the current solution
        must be considered.
        
        """
        distance : int = distances[current_node.id][node.id]
        return max(node.readytime, current_value + distance) + max(0, current_value + distance - node.duedate)
    
    
    
    
    @staticmethod
    def _bra (length : int, alpha : float) -> int:
        """
        This method implements the biased randomisation by returning an 
        element form a list, according to a quasi-geometric function.
                                f(x) = (1 - alpha)^x
        
        :param length: the length of the list of options
        :param alpha: the parameter of the quasi-geometric
        :return: the position in the list of the selected element
        
        """
        return int(math.log (random.random(), 1 - alpha)) % length
    
    
        
        
        
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.
        
        Node-by-node, until the solution is not complete, a new node is selected according to
        the biased randomisation and included in the solution. Then, the value and the delay of 
        the solution are updated, and the selected node is removed from the list of the 
        future options.
        
        According to the parameter beta the tour can also be modified just in part, but always starting from the bottom.
        
        """
        current_tour : List[Node] = tour[:int(len(tour)*(1.0 - self.beta))]
        solution : Solution = Solution ([], current_value, 0) if not current_tour else evaluate(current_tour, current_value, current_node, distances)
        current = current_node if not current_tour else solution.result[-1]
        selectables : List[Node] = [i for i in tour if not i in current_tour]
        
        while len(selectables) > 0:
            options = sorted(selectables, key=lambda n : self._costof (n, current, solution.value, distances))
            next_node : Node = options[self._bra(len(options), self.alpha)]
            selectables.remove (next_node)
            solution.result.append (next_node)
            solution.value += distances[current.id][next_node.id] + max(0, next_node.readytime - solution.value - distances[current.id][next_node.id])
            solution.delay += max(0, solution.value - next_node.duedate)
            current = next_node
        
        self.set_best_solution (solution)
        
        
        
        
        
        

        
        
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
    
    
    
    def __init__ (self, alpha : float = 0.9, starting_beta : float = 0.1, delta_beta : float = 0.1, iter : int = 1000):
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
        
        
        
        
    
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.
        
        Until the number of iterations defined is not elapsed a new solution
        is constructed via Biased Randomised Algorithm.
        At the end of the process, only the best solution found so far is kept.
        
        """
        builder : Greedy = Greedy(self.alpha, self.starting_beta)
        best : Solution = evaluate (tour, current_value, current_node, distances)

        for i in range (self.iter):
            builder.exe (current_value, tour, current_node, distances)
            new_sol : Solution = builder.get_best_solution
            
            if new_sol.cost < best.cost:
                best = new_sol
                builder.beta = self.starting_beta
            else:
                builder.beta = min(1.0, builder.beta + self.delta_beta)

        self.set_best_solution (best)
        
        
        
        
        

class SimulatedAnnealing (Algorithm):
    """
    This algorithm is the implementation of a Simulated Annealing.
    
    At the beginning of each era a random solution is generated.
    Then, for each iteration a new solution is generated and eventually
    made the new best. After generating a new solution the temperature
    is linearly decreased and the process is repeated.
    
    For generating a new solution two methods are used (i.e. swap and 2-opt).
    At each iteration the selection of the method is made according to their 
    probabilities.
    
    """
    
    
    def __init__ (self,
                  era : int = 1000,
                  max_temperature : float = 1.0,
                  min_temperature : float = 0.0,
                  step : float = 0.05,
                  neighbour_prob : Tuple[float, float] = (0.5,0.5),
                  greedy_start : bool = False
                 ) -> None:
        """
        Initialize.
        
        :param era: The number of eras.
        :param max_temperature: The max temperature at the beginning of each era (must be between 1 and 0).
        :param min_temperature: The min reachable temperature (must be between 1 and 0).
        :param step: The decrease of temperature at each iteration.
        :param neighbour_prob: The probability to use each of the neighbour seach methods (respectively swap and 2-opt)
        :param greedy_start: If true the algorithm starts from a already good greedy solution.
        
        """
        super().__init__()
        
        self.era = era
        self.max_t = max_temperature
        self.min_t = min_temperature
        self.step = step
        
        self.neighbour_method_prob = neighbour_prob if neighbour_prob[0] + neighbour_prob[1] == 1.0 else (neighbour_prob[0], 1 - neighbour_prob[0])
        self.greedy_start = greedy_start
        
        
    
    
    
        
    def _neighbour_search (self, tour : List[Node]) -> List[Node]:
        """
        This is the neighbour search method.
        Two different neighbour searches are implemented and at each iteration
        the selection is of the neighbour search method is random. The first
        method is a simple swap of two randomly selected nodes, the second one
        is the well-known 2-opt algorithm.
        
        :param tour: the current tour of nodes
        :return: a new tour of nodes
        
        """
        rnd = random.random()
        if rnd < self.neighbour_method_prob[0]:
            i, j = random.randint(0, len(tour)-1), random.randint(0, len(tour)-1)
            tour[i], tour[j] = tour[j], tour[i]
            return tour
        else:
            i, j = random.randint(0, len(tour)-1), random.randint(0, len(tour)-1)
            i, j = min(i,j), max(i,j)
            return tour[:i] + list(reversed(tour[i:j])) + tour[j:]
        
    
    
    
    
    
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.
        For each era a new random solution is generated. Then, for each iteration
        a new solution is generated via neighbour search. If the new solution is better
        than the best one, or if it is worst but the probability acceptance allows it,
        it is made the new best.
        
        """
        g = Greedy()
        g.exe (current_value, tour, current_node, distances)
        
        current_tour : List[Node] = tour
        current_sol : Solution = evaluate (tour, current_value, current_node, distances) if self.greedy_start is False else g.get_best_solution
        best : Solution = evaluate (tour, current_value, current_node, distances) if self.greedy_start is False else g.get_best_solution
        for era in range(self.era):
            random.shuffle (current_tour)
            current : Solution = evaluate (current_tour, current_value, current_node, distances)
            for i in numpy.arange (self.max_t, self.min_t, -self.step):
                current_tour = self._neighbour_search(current_tour)
                new_sol : Solution = evaluate (current_tour, current_value, current_node, distances)
                rnd_acceptance : float = random.random()
                if new_sol.cost < current_sol.cost or (new_sol.cost >= current_sol.cost and rnd_acceptance < i):
                    current_sol = new_sol
                    if current_sol.cost < best.cost:
                        best = current_sol
        self.set_best_solution (best)

        
        
        
        
        
        
        
        
        
class DaSilva (Algorithm):
    """
    This is the implementation of a two-phase heuristic proposed by Da Silva and Urrutia (2010) in
    
    Da Silva, R.F., Urrutia, S. (2010) "A General VNS heuristic for the traveling salesman problem 
    with time windows". Discrete Optimization. Vol. 7, pp. 203-211.
    
    """
    
    
    
    def __init__ (self, iter : int, maxlevel : int) -> None:
        """
        Initialize.
        
        :param iter: The maximum number of iterations of the algorithm.
        :param maxlevel: The strength of the perturbation procedure during
                         the feasible solutions' generation.
        
        """
        super().__init__()
        
        self.iter = iter
        self.maxlevel = maxlevel



    @staticmethod
    def evaluate (tour : List[Node], current_value : int, current_node : Node, distances : Dict[int,Dict[int,int]]) -> Tuple[Solution,Dict[str,List[Node]]]:
        violation_report : Dict[str,List[Node]] = {"violated":[], "notviolated":[]}
        solution : Solution = Solution(tour, current_value, 0)
        current : Node = current_node
        for node in tour:
            solution.value = max(node.readytime, solution.value + distances[current.id][node.id])
            solution.delay += max(0, solution.value - node.duedate)

            if solution.value - node.duedate > 0:
                violation_report["violated"].append(node)
            else:
                violation_report["notviolated"].append(node)

            current = node
        return solution, violation_report
    
    
    
    
    @staticmethod
    def _perturbation (tour : List[Node], level : int) -> List[Node]:
        tour = list(tour)
        for _ in range(level):
            i = random.randint(0, len(tour) - 1)
            extracted = tour.pop (i)
            j = min(max(random.choice([i-1, i+1]), 0), len(tour)-1)
            tour.insert (j, extracted)

        return tour
    


    @staticmethod
    def _one_shift (tour : List[Node], violated_report : Dict[str,List[Node]]) -> List[Node]:
        tour = list(tour)
        if len(violated_report.get("violated")) > 0:
            moved = random.choice(violated_report["violated"])
            i = tour.index(moved)
            tour.pop(i)
            tour.insert (i - 1, moved)
        return tour


        
    
    
    def _feasible_solution (self,
                           current_value : int,
                           tour : List[Node],
                           current_node : Node,
                           distances : Dict[int,Dict[int,int]]) -> Solution:
        """
        This method generates an always feasible solution.
        
        """
        level = 1
        random.shuffle (tour)
        current_sol, violated = self.evaluate (tour, current_value, current_node, distances)
        new_tour : List[Node]
        new_sol : Solution
        new_violated : Dict[str, List[Node]]
        
        while level < self.maxlevel and current_sol.delay > 0:

            new_tour = self._perturbation (tour, 1) #(tour, level)
            _, new_violated = self.evaluate (new_tour, current_value, current_node, distances)
            new_tour = self._one_shift (new_tour, new_violated)
            new_sol, new_violated = self.evaluate (new_tour, current_value, current_node, distances)
            
            if current_sol.delay < new_sol.delay:
                level += 1
            else:
                level = 1
                tour, current_sol, violated = new_tour, new_sol, new_violated

        return current_sol
    
    
    
    

    
    
    
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int,Dict[int,int]]) -> None:
        """
        This is the execution method.
        
        """
        best : Solution = evaluate (tour, current_value, current_node, distances)
        newsol : Solution
        
        for _ in range (self.iter):
            newsol = self._feasible_solution (current_value, tour, current_node, distances)
            #newsol = self._GVNS (newsol)
            
            if best.cost > newsol.cost:
                best = newsol
        
        self.set_best_solution (best)