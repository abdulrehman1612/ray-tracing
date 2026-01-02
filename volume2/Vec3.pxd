#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 04:19:30 2025

@author: AGU
"""

cdef class vec3:
    cdef double e[3]
    cpdef double x(self)
    cpdef double y(self)
    cpdef double z(self)
    cpdef double length(self)
    cpdef double length_squared(self)
    cpdef bint near_zero(self)


    