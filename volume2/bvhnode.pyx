#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 19:33:34 2025

@author: AGU
"""

from aabb cimport AABB
from ray cimport ray
from hittable import hit_record

cdef class BVHNode:
    
    cdef AABB box
    cdef BVHNode le
    cdef BVHNode ri
    cdef obj
    
    def __init__(self, aabb, left=None, right=None, objs=None):
        
        self.box = aabb
        self.le = left 
        self.ri = right
        self.obj = objs
    
    cpdef axis_min(self):
        return self.aabb.axis_min()
    
    cpdef axis_max(self):
        return self.aabb.axis_max()
    
    
    cpdef objects(self):
        return self.obj
    
    cpdef aabb(self):
        return self.box
    
    cpdef left(self):
        return self.le
    
    cpdef right(self):
        return self.ri


cpdef bint hit_BVH(BVHNode node,ray r, double ray_tmin, double ray_tmax, object rec):
    
    cdef double closest
    cdef object temp
    cdef bint hit_anything
    
    closest = ray_tmax
    temp = hit_record()
    hit_anything = False
    
    if node.objects() != None:
        if node.objects()[0].hit(r, ray_tmin, closest, temp):
            hit_anything = True
            closest = temp.t
            rec.copy_from(temp)
        return hit_anything
    
    if not node.aabb().hit(r, ray_tmin, ray_tmax):
        return False

    if hit_BVH(node.left(), r, ray_tmin, closest, rec):
        hit_anything = True
        closest = rec.t
    
    if hit_BVH(node.right(), r, ray_tmin, closest, rec):
        hit_anything = True
        
    return hit_anything

