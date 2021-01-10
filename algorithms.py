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
import itertools
import matplotlib.pyplot as plt


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
        self.set_best_solution (self.evaluate (tuple(tour), current_value, current_node, distances))











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
        
        
        
        
        
    def exe (self, current_value, tour, current_node, distances):
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
    
    def __init__ (self, alpha = 0.999, beta = 1.0):
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
    def _costof (node, current_node, current_value, distances):
        """
        This is the cost method used to evaluate the nodes and define their probability
        to be selected. Obviously, only nodes not included yet in the current solution
        must be considered.
        
        """
        distance = distances[current_node.id][node.id]
        return max(node.open, current_value + distance) - max(0, current_value + distance - node.close)
    
    
    
    
    @staticmethod
    def _bra (lst, alpha):
        """
        This method implements the biased randomisation by returning an 
        element form a list, according to a quasi-geometric function.
                                f(x) = (1 - alpha)^x
        
        :param lst: the list of options
        :param alpha: the parameter of the quasi-geometric
        :return: the position in the list of the selected element
        
        """
        return lst[int(math.log (random.random(), 1 - alpha)) % len(lst)]
    
    
        
        
        
    def exe (self, current_value, tour, current_node, distances):
        """
        This is the execution method.
        
        Node-by-node, until the solution is not complete, a new node is selected according to
        the biased randomisation and included in the solution. Then, the value and the delay of 
        the solution are updated, and the selected node is removed from the list of the 
        future options.
        
        According to the parameter beta the tour can also be modified just in part, but always starting from the bottom.
        
        """
        current_tour = tour[:int(len(tour)*(1.0 - self.beta))]
        solution, value, delay = [], current_value, 0 
        if len(current_tour) > 0:
            s = self.evaluate(current_tour, current_value, current_node, distances)
            solution, value, delay = s.result, s.value, s.delay
            solution = list(solution)

        current = current_node if not current_tour else solution[-1]
        selectables = [i for i in tour if not i in current_tour]
        
        while len(selectables) > 0:
            options = sorted(selectables, key=lambda n : self._costof (n, current, value, distances))
            next_node = self._bra(options, self.alpha)

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
    
    
    
    def __init__ (self, alpha=0.9, starting_beta=0.1, delta_beta=0.1, iter=1000):
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
        
        
        
        
    
    def exe (self, current_value, tour, current_node, distances):
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
                  era = 1000,
                  cooling = 0.9,
                  perturbation = 0.1,
                  perturbed = 0.1,
                  tabusize = 10):
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

        self.t = 10
        self.tabu = set()



    def shiftleft(self, tour):
        pass

    def shiftright (self, tour):
        pass

    def opt (self, tour):
        pass

    def swap (self, tour):
        pass




    def localsearch (self, tour, current_value, current_node, distances):
        """
        Generation of another solution in the neighbourhood.

        """
        func = random.choice((self.shiftleft, self.shiftright, self.opt, self.swap))
        tour = func(tour)

        # Eventual perturbation
        if (r := random.random()) < self.perturbation:
            for _ in range(int(len(tour) * self.perturbed)):
                removed_node = tour.pop(random.randint(0, len(tour) - 1))
                tour.insert(random.randint(0, len(tour) - 1), removed_node)

        return self.evaluate(tuple(tour), current_value, current_node, distances)








    def exe (self, current_value, tour, current_node, distances):

        # Preprocessing
        dists = copy.deepcopy(distances)
        for n1, n2 in itertools.product(tour, tour, repeat=1):
            if n1 is not n2:
                if n1.open + distances[n1.id][n2.id] > n2.close:
                    dists[n1.id][n2.id] = -1

        # Sort nodes by ascending closing time
        tour.sort(key=lambda i: i.close)

        # Starting solution
        x = self.evaluate(tuple(tour), current_value, current_node, distances)

        for _ in range (self.era):
            # New solution in the neighbourhood
            x_new = self.localsearch (tour, current_value, current_node, distances)

            # Eventually update the best
            r = random.random()
            if (i := cost(x_new)) < (j := cost(x)) or r > math.exp(- (i-j) / self.t):
                x = x_new

            # Update the temperature
            self.t *= 0.9

        self.set_best_solution(x)