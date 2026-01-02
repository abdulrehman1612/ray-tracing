#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 23:01:23 2025

@author: AGU
"""

from math import floor
import numpy as np
from numba import njit

class perlin:
    def __init__(self):
        self.randomvec = [[np.random.uniform(-1,1),np.random.uniform(-1,1),np.random.uniform(-1,1)] for i in range(256)]
        self.perm_x = [0] * 256
        self.perm_y = [0] * 256
        self.perm_z = [0] * 256
        

        perlin_generate_perm(self.perm_x)
        perlin_generate_perm(self.perm_y)
        perlin_generate_perm(self.perm_z)
        
        
    def noise(self, p):
        u = p.x() - floor(p.x())
        v = p.y() - floor(p.y())
        w = p.z() - floor(p.z())

        
        i = int(floor(p.x()))
        j = int(floor(p.y()))
        k = int(floor(p.z()))
        c = np.empty((2, 2, 2, 3), dtype=np.float64)

        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di][dj][dk] = self.randomvec[self.perm_x[(i+di) & 255] ^ self.perm_y[(j+dj) & 255] ^ self.perm_z[(k+dk) & 255]]
        
        return perlin_interp(c, u, v, w)
                    
    
    def terbulance(self, p, depth):
        accum = 0
        temp_p = p
        weight = 1
        
        for i in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2
        
        return abs(accum)
    
    



    
@njit
def perlin_interp(c, u, v, w):
    uu = u*u*(3-2*u)
    vv = v*v*(3-2*v)
    ww = w*w*(3-2*w)
    accum = 0
    
    for i in range(2):
        for j in range(2):
            for k in range(2):
                weight_v = [u-i, v-j, w-k]
                accum += (i*uu + (1-i)*(1-uu)) * (j*vv + (1-j)*(1-vv)) * (k*ww + (1-k)*(1-ww)) *  ((c[i,j,k,0]) * weight_v[0] + (c[i,j,k,1]) * weight_v[1] + (c[i,j,k,2]) * weight_v[2])
    return accum
     
@njit
def perlin_generate_perm(p):
    for i in range(256):
        p[i] = i
    for i in range(255, 0,-1):
        target = np.random.randint(0, i)
        p[i], p[target] = p[target], p[i]