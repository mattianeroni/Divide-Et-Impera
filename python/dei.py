from __future__ import annotations
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
from typing import List, Tuple, Optional, Sequence, Set, Dict, Union, cast

import random
import copy

from abc import ABC, abstractmethod
from dataclasses import dataclass






@dataclass
class Node:
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

    id : int
    x : int
    y : int
    readytime : int
    duedate : int



    @property
    def position (self) -> Tuple[int,int]:
        """
        This property returns the position of the node as a <tuple> indicating its
        x and y coordinates.

        """
        return self.x, self.y
    





@dataclass
class Solution:
    """
    This class represents a solution of the algorithm.


    :attr result: the solution in itself represented as a <list>, where each element
                    is the ID of the node to visit in that position.
    :attr value: the cost of the solution (i.e. total travel time, makespan)
    :attr delay: the delay cumulated during the tour.

    """
    result : List[Node]
    value : int
    delay : int




    @property
    def cost (self) -> int:
        """
        The cost of the solution is calculated considering:
            - The travel time.
            - The cumulated waiting time every time a node is reached before its opening time.
            - The cumulated delay as a sort of Lagrangian relaxation to penalise the solutions
              that reach the nodes after the closing time. 

        """
        return self.value + self.delay





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


    def __init__(self) -> None:
        """
        Initialize.

        It only initialize the best solution.
        """

        self._bestsolution : Solution




    @abstractmethod
    def exe (self, current_value : int, tour : List[Node], current_node : Node, distances : Dict[int, Dict[int, int]]) -> None:
        """
        This is the method to override for the execution of the algorithm.
        All the main procedure of the implemented algorithm must be written in this method.

        This method do not must return something.
        The best solution found with the procedure will be returned next by using get_best_solution property.

        :param tour: the nodes to visit
        :param current_node: the starting node to compleate the tour
        :param distances: the distance matrix of the graph

        """
        pass




    @property
    def get_best_result (self) -> Tuple[List[int], int, int]:
        """
        This property returns the best solution found so far, its cost, and the cumulated delay.
        If the best solution has not been set already, an Exception is returned.

        :return: <result>, <value>, <delay>

        """

        if not self._bestsolution:
            raise BestNotDefined

        return [node.id for node in self._bestsolution.result], self._bestsolution.value, self._bestsolution.delay





    @property
    def get_best_solution (self) -> Solution:
        """
        This property returns the best solution found so far by returning the solution
        instance in itself with all its attributes.
        If the best solution has not been set already, an Exception is raised.

        :return: the current best solution

        """

        if not self._bestsolution:
            raise BestNotDefined

        return self._bestsolution





    def set_best_solution (self, best : Solution) -> None:
        """
        This method sets the best solution of the algorithm.
        """

        self._bestsolution = copy.copy(best)








def euclidean (node1 : Node, node2 : Node) -> int:
    """
    This function calculates the euclidean distance between two nodes.

    To be processed by this function, the nodes must be data structures equal
    to that one handled by the DivideEtImpera (DEI) algorithm (see Node class).

    :param node1: The first node
    :param mode2: The second node
    :return: the euclidean distance rounded to 0 decimals.

    """
    return int(((node1.x - node2.x)**2 + (node1.y - node2.y)**2)**0.5)








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
                algorithm : Algorithm,
                nodes : Sequence[Node], 
                p : int,
                max_split : int = 10,
                base_node_id : int = 0,
                goback : bool = True
                ):
        """
        Initialize.

        Before initializing the algorithm a control is made. If the base_node (i.e. the source node)
        is not in the list of nodes provided, an Exception is raised.

        :param algorithm: The included algorithm to solve the subsets
        :param nodes: The nodes of the problem
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

        found_base = False
        base_node : Node

        for node in nodes:
            if node.id == base_node_id:
                found_base = True
                base_node = node
                break


        if found_base is False:
            raise BaseNotFound(str(base_node_id) + ' is not in nodes list')




        self.algorithm = algorithm
        self.p = p
        self.max_split = max_split
        self.goback = goback

        self.base_node : Node = base_node
        self.current_node : Node = base_node
        
        self.distances : Dict[int, Dict[int, int]] = {i.id : {j.id : euclidean(i,j) for j in nodes} for i in nodes}
        
        self.tour : List[Node] = list(nodes)
        self.tour.remove(base_node)
        
        self.solution = Solution([], 0, 0)





    def _reset (self) -> None:
        """
        This <private> method reset the current solution of the algorithm.
        It should be used to build a new one.

        """
        self.solution = Solution ([], 0, 0)
        self.current_node = self.base_node






    def exe (self, tour : Optional[List[Node]] = None) -> Solution:
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

        :param tour: <list> The list of nodes
        :return: The solution

        """

        tour = tour or self.tour

        if len(tour) > self.p:

            split : int = 0
            first_part : List[Node] = []
            second_part : List[Node] = []


            while (not first_part or not second_part) and split < self.max_split:

                partition_node = random.choice(tour)

                split += 1

                first_part = [node for node in tour if node.duedate < partition_node.readytime]
                second_part = [node for node in tour if node.duedate >= partition_node.readytime]



            if len(first_part) is 0 or len(second_part) is 0:
                self._solve_tour (tour)

            else:
                self.exe (first_part)
                self.exe (second_part)


        else:
            self._solve_tour (tour)




        return self.solution







    def _solve_tour (self, tour : List[Node]) -> None:
        """
        This <private> method executes the algorithm on a subset of the nodes, and 
        updates the current solution.

        :param tour: The subset of nodes

        """

        self.algorithm.exe(self.solution.value, tour, self.current_node, self.distances)
        sol : Solution = self.algorithm.get_best_solution

        self.solution.result.extend(sol.result)
        self.solution.value = sol.value
        self.solution.delay += sol.delay

        self.current_node = sol.result[-1]

        if self.goback and len(self.solution.result) == len(self.tour):
            self.solution.value += self.distances[self.current_node.id][self.base_node.id]







    def metaheuristic (self, maxiter=1000) -> Solution:
        """
        This method is a metaheuristic implementation of the DEI algorithm.

        It simply repeats the DEI more and more times until the maximum number
        of iterations is note elapsed.
        
        :param maxiter: The number of iterations that the algorithm is repeated.
        :return: The best solution found.

        """

        best : Optional[Solution] = None

        for i in range(maxiter):
            self._reset()
            sol = self.exe()

            if not best or best.cost > sol.cost:
                best = sol

        return cast(Solution, best)
