# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 23:47:07 2025

@author: rehma
"""

import numpy as np
import random
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
    
    def near_zero(self):
        s = 1e-8
        return ((abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s))
    
    def __pow__(self, exponent):
        return vec3(*(self.e ** exponent))

    def __repr__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"
    
    #Random vectors
    def random(a=-1,b=1):
        return vec3(random.uniform(a,b),random.uniform(a,b),random.uniform(a,b))
    
    
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

def random_unit_vector():
    while True:
        p = vec3.random()
        lensq = p.length_squared()
        if (1e-160 < lensq <= 1):
            return (p/(lensq**0.5))
def random_on_hemisphere(normal):
    on_unit_sphere = vec3.random_unit_vector()
    if (dot(on_unit_sphere, normal)>0):
        return on_unit_sphere
    else:
        return -on_unit_sphere

def reflect(v, n):
    return v - 2*dot(v,n)*n

def refract(r:vec3, n: vec3, etai_over_etat: float):
    cos_theta = min(dot(-r, n), 1.0)
    r_out_perp =  etai_over_etat * (r + cos_theta*n)
    r_out_parallel = -((abs(1.0 - r_out_perp.length_squared()))**0.5) * n
    return r_out_perp + r_out_parallel
    
def reflectance(cosine,refraction_index):
        r0 = ((1 - refraction_index)/(1 + refraction_index))
        r0 = r0*r0
        return r0 + (1-r0)*((1 - cosine)**5)
