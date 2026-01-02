#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 02:57:34 2025

@author: AGU
"""



cdef class ray:
    
    
    def __init__(self, a, b, double t = 0):
        self.orig = a
        self.direc = b
        self.te = t
    
    cpdef origin(self):
        return self.orig
    
    cpdef direction(self):
        return self.direc
    
    cpdef double time(self):
        return self.te
    
    cpdef at(self, double t):
        return self.orig + t * self.direc