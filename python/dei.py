from algorithm import Solver
from typing import Tuple, Optional, Generator, Deque, cast
from node import Node
from solution import Solution

import numpy as np  #type: ignore
import collections
import random


class DivideEtImpera (object):

    def __init__ (self, solver : Solver,
                        nodes : Tuple[Node, ...],
                        dists : np.array,
                        p : int = 30,
                        maxtrysplit : int = 1000

                        ) -> None:

        self.solver = solver
        self.nodes = nodes
        self.dists = dists
        self.p = p
        self.maxtrysplit = maxtrysplit

        self.current_node : Optional[Node] = None
        self.travel_time = 0
        self.delay = 0
        self.tour : Deque[Node] = collections.deque([], maxlen=len(nodes))

        self.best : Optional[Solution] = None


    def solve (self, tour : Tuple[Node, ...]) -> None:
        s = self.solver
        s.solve(tour, self.dists, cast(Node, self.current_node), self.travel_time)
        self.tour.extend(s.tour)
        self.travel_time = s.travel_time
        self.delay += s.delay
        self.current_node = s.tour[-1]


    def __call__(self, tour : Optional[Tuple[Node, ...]] = None) -> Solution:
        tour = tour or self.nodes
        if self.current_node is None:
            self.current_node = tour[0]

        if len(tour) > self.p:
            first : Tuple[Node, ...]
            second : Tuple[Node, ...]
            for _ in range(self.maxtrysplit):
                pivot = random.choice(list(tour))
                first = tuple(n for n in tour if n.close < pivot.open)
                second = tuple(set(first) - set(tour))

                if len(first) > 0 and len(second) > 0:
                    self.__call__(first)
                    self.__call__(second)
                    break
            else:
                self.solve(tour)
        else:
            self.solve(tour)

        self.best = Solution(self.tour, self.travel_time, self.delay)
        return self.best
