from __future__ import annotations
"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node, cost



"""
Libraries imported from Python 3 standard library.
"""
import random
import copy
import itertools
import math
import collections

from typing import Tuple, Dict, List, Optional, cast, Deque, Callable




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
