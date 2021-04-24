import abc
import numpy as np #type: ignore

from node import Node
from typing import Tuple
from solution import Solution



class Solver(abc.ABC):

    @abc.abstractproperty
    def best (self) -> Solution:
        ...

    @abc.abstractproperty
    def tour (self) -> Tuple[Node]:
        ...

    @abc.abstractproperty
    def travel_time (self) -> int:
        ...

    @abc.abstractproperty
    def delay (self) -> int:
        ...

    @abc.abstractmethod
    def solve (self, tour : Tuple[Node, ...], dists : np.array, cnode : Node, travel_time : int) -> None:
        ...
