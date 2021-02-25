from __future__ import annotations
"""
Libraries imported from Python 3 standard library.
"""
import random

from typing import Tuple, Dict, List, Optional, cast


"""
Import from the DivideEtImpera package which imports the Algorithm
abstract class from which all these algorithms must inherit, the
Solution class, and the Node class.

"""
from dei import Algorithm, Solution, Node, cost






class ParticleSwarmOptimization (Algorithm):
    """
    This is a readaped implementation of the Particle Swarm Optimization.

    """

    def __init__ (self,
                  era : int = 1000,
                  particles : int = 30,
                  greediness : float = 0.1,
                  beta : float = 0.9,
                  deepsearch : float = 0.1,
                  fulldeepsearch : float = 0.2
                  ) -> None:
        """
        Initialize.

        :param era: The number of iterations of the algorithm.
        :param particles: The number of particles
        :param greediness: The weight given to the greedy solution.
        :param beta: The parameter of the quasi-geometric used to generate the
                    intention of the particles.
        :param deepsearch: The probability of deepsearch.
        :param fulldeepsearch: The probability to do a full deepsearch.

        """
        self.era = era
        self.particles = particles
        self.greediness = greediness
        self.beta = beta
        self.deepsearch = deepsearch
        self.fulldeepsearch = fulldeepsearch
