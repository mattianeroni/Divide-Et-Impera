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
import numpy
import matplotlib.pyplot as plt


"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node, cost








def evaluate (tour, current_value, current_node, distances):
    """
    This function can be used by all the algorithms implemented
    in this library to evaluate a solution, once the nodes to visit
    have been set in the desired order.
    Given the tour, the current value, and the current node, the function 
    returns a solution after calculating its value and delay.
    
    """
    value, delay = current_value, 0
    current = current_node
    for node in tour:
        value = max(node.open, value + distances[current.id][node.id])
        delay += max(0, value - node.close) 
        current = node
    return Solution(tour, value, delay)
    
    
    
    
    





class Shuffler (Algorithm):

    """
    This algorithm randomly shuffle the nodes to visit, by generating in this way 
    a random tour.
    After that, the cost of the solution is calculated.

    """



    def __init__ (self):
        """
        Initialize.
        """
        super().__init__()





    def exe (self, current_value, tour, current_node, distances):
        """
        This is the execution method of the algorithm.

        """

        random.shuffle (list(tour))
        self.set_best_solution (evaluate (tuple(tour), current_value, current_node, distances))











class RandomSearch (Algorithm):

    """
    This algorithm randomly shuffle the nodes to visit more and more times, by
    generating in this way more random tours.
    At each iteration, the algorithm keeps track of the best solution found
    so far.
    Finally, the best solution found is returned.

    """



    def __init__ (self, iter = 1000):
        """
        Initialize.

        :param iter: The number of iterations and solutions exlored 
                     by the algorithm during its execution.

        """
        super().__init__()
        self.iter = iter





    def exe (self, current_value, tour, current_node, distances):
        """
        This is the execution method of the algorithm. It inherits from the exe abstract
        method in the Algorithm abstract class.

        """
        s = Shuffler()
        best = evaluate (tour, current_value, current_node, distances)
        i = 0

        while i < self.iter:
            s.exe (current_value, tour, current_node, distances)
            solution = s.get_best_solution
            i += 1
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
    
    def __init__ (self, iter, deep = False):
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
