#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 19:36:49 2025

@author: AGU
"""

from Vec3 cimport vec3

cdef class AABB:
    cdef vec3 cen
    cdef vec3 min_
    cdef vec3 max_
    
    cpdef axis_min(self)
    
    cpdef axis_max(self)
    
    cpdef center(self)
    
    cpdef bint hit(self, r, double ray_tmin, double ray_tmax)