#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 19:51:40 2025

@author: AGU
"""


cdef class ray:
    cdef direc
    cdef orig
    cdef double te
    cpdef origin(self)
    cpdef direction(self)
    cpdef double time(self)
    cpdef at(self, double t)