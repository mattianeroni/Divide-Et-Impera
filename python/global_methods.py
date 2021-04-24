import numpy as np #type: ignore

from typing import Tuple, Any
from node import Node



def evaluate (tour : Tuple[Node], dists : np.array, current_node : Node, current_time : int) -> Tuple[Tuple[Node], int, int]:
    cnode = current_node
    delay = 0
    for node in tour:
        current_time = max(node.open, current_time + dists[cnode.id, node.id])
        delay += max(0, current_time - node.close)
        cnode = node

    return tour, current_time, delay
