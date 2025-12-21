# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 23:47:07 2025

@author: rehma
"""

import numpy as np

class vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.e = np.array([x, y, z], dtype=float)

    # Getters
    def x(self): return self.e[0]
    def y(self): return self.e[1]
    def z(self): return self.e[2]

    # Indexing
    def __getitem__(self, i):
        return self.e[i]

    def __setitem__(self, i, value):
        self.e[i] = value

    # Unary minus
    def __neg__(self):
        return vec3(*( -self.e ))

    # u + v
    def __add__(self, other):
        return vec3(*(self.e + other.e))

    # u - v
    def __sub__(self, other):
        return vec3(*(self.e - other.e))

    # u * v (component-wise) or v * scalar
    def __mul__(self, other):
        if isinstance(other, vec3):
            return vec3(*(self.e * other.e))   # component-wise
        return vec3(*(self.e * other))         # scalar multiply

    # scalar * v
    def __rmul__(self, other):
        return vec3(*(other * self.e))

    # v / scalar
    def __truediv__(self, t):
        return vec3(*(self.e / t))

    # Length & squared length
    def length(self):
        return np.linalg.norm(self.e)

    def length_squared(self):
        return np.dot(self.e, self.e)

    def __repr__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"

# Aliases
point3 = vec3
color = vec3

# Utility functions
def dot(u, v):
    return float(np.dot(u.e, v.e))

def cross(u, v):
    return vec3(*np.cross(u.e, v.e))

def unit_vector(v):
    return v / v.length()
