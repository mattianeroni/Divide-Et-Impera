import dataclasses
import math

@dataclasses.dataclass(frozen=True, eq=True, unsafe_hash=True)
class Node:
    id : int
    x : int
    y : int
    open : int
    close : int

    def __sub__ (self, other):
        return math.sqrt(math.pow(self.y - other.y, 2) + math.pow(self.x - other.x, 2))
