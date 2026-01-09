#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 01:22:07 2026

@author: AGU
"""
from Vec3 import vec3

class sphere:
    def __init__(self, center1, radius, material, center2 = vec3(0,0,0)):
        
        self.center1 = center1
        self.center2 = center2
        self.radius = radius
        self.material = material
        self.type = 0
        
        cen1 = self.center1
        cen2 = self.center1 + self.center2
        max_cen1 = vec3(cen1.x()+self.radius, cen1.y()+self.radius, cen1.z()+self.radius)
        min_cen1 = vec3(cen1.x()-self.radius, cen1.y()-self.radius, cen1.z()-self.radius)
        max_cen2 = vec3(cen2.x()+self.radius, cen2.y()+self.radius, cen2.z()+self.radius)
        min_cen2 = vec3(cen2.x()-self.radius, cen2.y()-self.radius, cen2.z()-self.radius)
        
        self.max = vec3(max(max_cen1.x(), max_cen2.x()),max(max_cen1.y(), max_cen2.y()),max(max_cen1.z(), max_cen2.z()))
        self.min = vec3(min(min_cen1.x(), min_cen2.x()),min(min_cen1.y(), min_cen2.y()),min(min_cen1.z(), min_cen2.z()))
        self.centroid = (self.max+self.min) * 0.5


class quad:
    def __init__(self, Q,U,V, material):
        self.Q = Q
        self.U = U
        self.V = V
        self.material = material
        self.type = 1
        
        max_cen1 = self.Q+self.U+self.V
        min_cen1 = self.Q
        max_cen2 = self.Q + self.V
        min_cen2 = self.Q + self.U
        
        self.max = vec3(max(max_cen1.x(), max_cen2.x()),max(max_cen1.y(), max_cen2.y()),max(max_cen1.z(), max_cen2.z()))
        self.min = vec3(min(min_cen1.x(), min_cen2.x()),min(min_cen1.y(), min_cen2.y()),min(min_cen1.z(), min_cen2.z()))
        self.centroid = (self.max+self.min) * 0.5
        