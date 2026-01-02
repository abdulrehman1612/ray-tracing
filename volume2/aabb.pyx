#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 04:14:22 2025

@author: AGU
"""

from Vec3 cimport vec3

cdef class AABB:
    
    
    def __init__(self, vec3 min_cords, vec3 max_cords):
        self.min_ = min_cords
        self.max_ = max_cords
        self.cen = (max_cords + min_cords)/2
    
    cpdef axis_min(self):
        return self.min_
    
    cpdef axis_max(self):
        return self.max_
    
    cpdef center(self):
        return self.cen
    
    cpdef bint hit(self, r, double ray_tmin, double ray_tmax):
        cdef double tmin, tmax, temp, t0, t1
        
        tmin = (self.min_.x() - r.origin().x()) / r.direction().x()
        tmax = (self.max_.x() - r.origin().x()) / r.direction().x()
        
        if 1/r.direction().x() < 0:
            temp = tmin
            tmin = tmax
            tmax = temp
        
        t0 = max(ray_tmin, tmin)
        t1 = min(ray_tmax, tmax)
        if t1 <= t0:
            return False
        
        tmin = (self.min_.y() - r.origin().y()) / r.direction().y()
        tmax = (self.max_.y() - r.origin().y()) / r.direction().y()
        if 1/r.direction().y() < 0:
            temp = tmin
            tmin = tmax
            tmax = temp
        t0 = max(t0, tmin)
        t1 = min(t1, tmax)
        if t1 <= t0:
            return False
        

        tmin = (self.min_.z() - r.origin().z()) / r.direction().z()
        tmax = (self.max_.z() - r.origin().z()) / r.direction().z()
        if 1/r.direction().z() < 0:
            temp = tmin
            tmin = tmax
            tmax = temp
        t0 = max(t0, tmin)
        t1 = min(t1, tmax)
        if t1 <= t0:
            return False
        
        return True