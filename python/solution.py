import dataclasses


from typing import Sequence
from node import Node


@dataclasses.dataclass(eq=True, frozen=True, unsafe_hash=True)
class Solution:
    nodes : Sequence[Node]
    travel_time : int
    delay : int
