# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 20:07:58 2025

@author: rehma
"""

from abc import ABC, abstractmethod
from ray import ray

class material(ABC):
    @abstractmethod
    def scatter():
        pass

        