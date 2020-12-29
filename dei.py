"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

DIVIDE ET IMPERA ALGORITHM


This algorithm is designed for Traveling Salesman Problem with Time Windows (TSPTW).
The algorithm aims at the optimization of the route, and is designed to be implemented in case of
very complex problems (i.e. when the list of nodes to visit is made of 100 elements or more).


The mechanism is based on the fact that a long set of nodes, in case of TSPTW, might be split
into two smaller subsets. Let's assume j = 1...N the nodes (i.e. customers) to visit, Sj the 
opening time of the node j, and Ej the closing time of the node j.
Once a generic node j is considered, the set of nodes might be split into two subsets simply
considering that all the nodes which close before Sj must be visited before j.
In this way, the generic node j works as a sort of PARTITION NODE, which is used to divide the big
set of nodes in two subsets smaller and easier to optimize.


This behaviour allows the optimization of a big problem dividing it in many smaller ones.
This might be helpful to improve the results and the computational time too.



Written by Mattia Neroni in June 2020.

Author contact: mattia.neroni@unipr.it.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""




"""
Libraries imported from Python 3 standard library.
"""
import random
import copy
import numpy as np

from abc import ABC, abstractmethod
from collections import namedtuple




"""
This class represent a node of the graph, which is representative of a 
customer or location to be visited within a certain time window, which
goes from its <readytime> to its <duedate>.

:attr id: The unique id of the node
:attr x: The x coordinate of the node
:attr y: The y coordinate of the node
:attr readytime: The starting time of the window in which the node is available
:attr duedate: The closing time of the window in which the node is available
"""
Node = namedtuple("Node", "id x y open close")







"""
This class represents a solution of the algorithm.

:attr result: the solution in itself represented as a <tuple>, where each element
              is the ID of the node to visit in that position.
:attr value: the cost of the solution (i.e. total travel time, makespan)
:attr delay: the delay cumulated during the tour.
"""
Solution = namedtuple("Solution", "result value delay")
    



    
    
    
def cost (solution):
    """
    The cost of the solution is calculated considering:
        - The travel time.
        - The cumulated waiting time every time a node is reached before its opening time.
        - The cumulated delay as a sort of Lagrangian relaxation to penalise the solutions
          that reach the nodes after the closing time. 
    """
    return solution.value + solution.delay






def euclidean (node1, node2):
    """
    This function calculates the euclidean distance between two nodes.

    To be processed by this function, the nodes must be data structures equal
    to that one handled by the DivideEtImpera (DEI) algorithm (see Node class).

    :param node1: The first node
    :param mode2: The second node
    :return: the euclidean distance rounded to 0 decimals.

    """
    return int(((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**0.5)







class BestNotDefined (Exception):
    """
    This exception is raised by the Algorithm class in case the attribute
    best solution is required before being defined.

    """
    pass





class BaseNotFound (Exception):
    """
    This exception is raise by the DivideEtImpera if the base_node is not in 
    the list of nodes to visit which has been provided.

    """
    pass







class Algorithm (ABC):
    """
    This is an abstract class the algorithms included in the Divide Et Impera must inherit from.
    
    It handles all the operations regarding the best solution, which must be standardized
    for an implementation in the DivideEtImpera.

    """


    def __init__(self):
        """
        Initialize.

        It only initialize the best solution.
        """
        self.__bestsolution = None




    @abstractmethod
    def exe (self, current_value, tour, current_node, distances):
        """
        This is the method to override for the execution of the algorithm.
        All the main procedure of the implemented algorithm must be written in this method.

        This method do not must return something.
        The best solution found with the procedure will be returned next by using get_best_solution property.
        
        :param current_value: The current time when started this part of the tour (necessary
                                for delays).
        :param tour: The nodes to visit
        :param current_node: The starting node to compleate the tour
        :param distances: The distance matrix of the graph

        """
        pass



    @staticmethod
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




    @property
    def get_best_result (self):
        """
        This property returns the best solution found so far, its cost, and the cumulated delay.
        If the best solution has not been set already, an Exception is returned.

        :return: <result>, <value>, <delay>

        """
        if not self.__bestsolution:
            raise BestNotDefined

        return self.__bestsolution.result, self.__bestsolution.value, self.__bestsolution.delay





    @property
    def get_best_solution (self):
        """
        This property returns the best solution found so far by returning the solution
        instance in itself with all its attributes.
        If the best solution has not been set already, an Exception is raised.

        :return: the current best solution

        """
        if not self.__bestsolution:
            raise BestNotDefined

        return self.__bestsolution





    def set_best_solution (self, best):
        """
        This method sets the best solution of the algorithm.
        """
        self.__bestsolution = copy.copy(best)






class DivideEtImpera:

    """
    This is the algorithm class.

    The characteristics of the algorithm are the following:
    - DivideEtImpera is a sort of heuristic framework based on conquer techniques of Giulio Cesare Roman Imperator.
    - This version is designed to solve the Traveling Salesman Problem with Time Windows (TSPTW).
    - The target are very big problems difficult to solve with a normal metaheuristic.
    - This framework can include both heuristic and metaheuristic techniques, and it can have both
        a heuristic or a metaheuristic behaviour.
    
    The algorithm included (e.g. a heuristic or a metaheuristic) must inherit from the Algorithm class written above.


    """

    def __init__(self,
                algorithm,
                nodes, 
                p = 30,
                max_split = 10,
                base_node_id = 1,
                goback = True):
        """
        Initialize.

        Before initializing the algorithm a control is made. If the base_node (i.e. the source node)
        is not in the list of nodes provided, an Exception is raised.

        :param algorithm: The included algorithm to solve the subsets
        :param nodes: The nodes of the problem contained in a dict indexed with the nodes id
        :param p: The only parameter of the DEI; it is the number of nodes of a subset
                  considered acceptable to solve it with the included algorithm.
        :param max_split: The maximum number of times the DEI tries to split a set in 2 subset, if
                 this number is overtaken, the set is considered as not splittable.
        :param base_node_id: The ID of the source node (by default the node with ID equal to 0)
        :param goback: If True at the end of the tour the truck must go back to the source node,
                       other wise not (by default it is True).

        :attr current_node: The node where the truck currently is. It increase as the solution is built.
        :attr base_node: The node the tour starts from (i.e. source node).
        :attr distances: A dictionary of dictionaries containing the distances from each node to each other.
        :attr tour: The list of nodes to visit. The source or base node is excluded.
        :attr solution: The current solution in building phase.

        """

        if (base:=nodes.get(base_node_id)):
            self.base_node = base
            
        else:
            raise BaseNotFound(str(base_node_id) + ' is not in nodes list')
            


        self.algorithm = algorithm
        self.p = p
        self.max_split = max_split
        self.goback = goback

        self.current_node = self.base_node
        
        self.distances = {i : {j : euclidean(nodes[i],nodes[j]) for j in nodes} for i in nodes}
        
        self.tour = tuple(n for n in nodes.values() if n != base_node)
        
        self.solution = None
        self.result, self.value, self.cost = [], 0, 0





    def _reset (self):
        """
        This <private> method reset the current solution of the algorithm.
        It should be used to build a new one.

        """
        self.solution = None
        self.current_node = self.base_node
        self.result, self.value, self.cost = [], 0, 0






    def exe (self, tour=None):
        """
        This method is the core of the algorithm.

        It is recursively repeated until the solution is not built. A tour must be passed to it,
        if it is not, the full set of nodes is considered and the algorithm starts.

        If the length of the tour is higher than the parameter p, a partition node is found and
        the set is divided into two smaller subsets. And the method is recersively repeated on
        each of these subsets beginning from the one to visit before.

        It might happen that, even if the tour is too long and must be divided, the partition
        node (which is uniformly selected) do not splits the tour. In this case, a new 
        partition node is selected, and this process is eventually repeated up to max_split
        times. If after max_split times, every partition node did not split the tour, the 
        tour is considered as not splittable, and it is solved by using the algorithm.

        :param tour: <tuple> The set of nodes
        :return: The solution

        """
        tour = tour or self.tour

        if len(tour) > self.p:
            
            split, max_split = 0, self.max_split
            first_part = tuple()
            second_part = tuple()


            while (not first_part or not second_part) and split < max_split:
                
                partition_node = random.choice(tour)
                split += 1

                first_part = tuple(node for node in tour if node.close < partition_node.open)
                second_part = tuple(node for node in tour if node.close >= partition_node.open)



            if len(first_part) == 0 or len(second_part) == 0:
                self._solve_tour (tour)
            else:
                self.exe (first_part)
                self.exe (second_part)

        else:
            self._solve_tour (tour)

        self.solution = Solution(self.result, self.value, self.cost)
        return self.solution







    def _solve_tour (self, tour):
        """
        This <private> method executes the algorithm on a subset of the nodes, and 
        updates the current solution.

        :param tour: The subset of nodes

        """

        self.algorithm.exe(self.solution.value, tour, self.current_node, self.distances)
        sol = self.algorithm.get_best_solution

        self.solution.result.extend(sol.result)
        self.solution.value = sol.value
        self.solution.delay += sol.delay

        self.current_node = sol.result[-1]

        if self.goback and len(self.solution.result) == len(self.tour):
            self.solution.value += self.distances[self.current_node.id][self.base_node.id]
