#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 01:22:07 2026

@author: AGU
"""
from Vec3 import vec3
from list_hittable import list_hittable

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
        
        p0 = self.Q
        p1 = self.Q + self.U
        p2 = self.Q + self.V
        p3 = self.Q + self.U + self.V
        
        min_x = min(p0.x(), p1.x(), p2.x(), p3.x())
        min_y = min(p0.y(), p1.y(), p2.y(), p3.y())
        min_z = min(p0.z(), p1.z(), p2.z(), p3.z())

        max_x = max(p0.x(), p1.x(), p2.x(), p3.x())
        max_y = max(p0.y(), p1.y(), p2.y(), p3.y())
        max_z = max(p0.z(), p1.z(), p2.z(), p3.z())
        
        self.min = vec3(min_x, min_y, min_z)
        self.max = vec3(max_x, max_y, max_z)
        self.centroid = (self.max+self.min) * 0.5

class box:
    def __init__(self, a, b, mat):
        self.sides = list_hittable()
        self.material = None
        
        min_ = vec3(min(a.x(),b.x()), min(a.y(),b.y()),min(a.z(),b.z()))
        max_ = vec3(max(a.x(),b.x()), max(a.y(),b.y()),max(a.z(),b.z()))
    
        dx = vec3(max_.x() - min_.x(), 0, 0);
        dy = vec3(0, max_.y() - min_.y(), 0);
        dz = vec3(0, 0, max_.z() - min_.z());
    
        self.sides.add(quad(vec3(min_.x(), min_.y(), max_.z()),  dx,  dy, mat))
        self.sides.add(quad(vec3(max_.x(), min_.y(), max_.z()), -dz,  dy, mat))
        self.sides.add(quad(vec3(max_.x(), min_.y(), min_.z()), -dx,  dy, mat))
        self.sides.add(quad(vec3(min_.x(), min_.y(), min_.z()),  dz,  dy, mat))
        self.sides.add(quad(vec3(min_.x(), max_.y(), max_.z()),  dx, -dz, mat))
        self.sides.add(quad(vec3(min_.x(), min_.y(), min_.z()),  dx,  dz, mat))
        
        self.min = min_
        self.max = max_
        self.centroid = (self.max+self.min) * 0.5
        