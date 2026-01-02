#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 03:00:38 2025

@author: AGU
"""

from hittable import hittable, hit_record
from ray import ray
from Vec3 import *
from aabb import AABB
from bvh import enclose


class triangle(hittable):
    def __init__(self, q1, u1, v1, material, q2 = None, u2 = None, v2 = None):
        self.Q =  ray(q1, vec3(0, 0, 0)) if (q2 is None) else ray(q1, q2 - q1)
        self.u = ray(u1, vec3(0, 0, 0)) if (u2 is None) else ray(u1, u2 - u1)
        self.v = ray(v1, vec3(0, 0, 0)) if (v2 is None) else ray(v1, v2 - v1)
        self.material = material
        self.aabb = triangle.enclose_quad(self.Q, self.u, self.v, (q2 == None and u2 == None and v2 == None))
        
    
    def enclose_quad(Q, U, V , flag):
        if flag:
            q = Q.origin()
            u = U.origin()
            v = V.origin()
            box1 = AABB(q, q+u+v)
            box2 = AABB(q+u, q+v)
            return enclose([box1, box2])
        
        else:
            q1 = Q.at(0)
            u1 = U.at(0)
            v1 = V.at(0)
            box1_1 = AABB(q1, q1+u1+v1)
            box1_2 = AABB(q1+u1, q1+v1)
            box1 = enclose([box1_1, box1_2])
            q2 = Q.at(1)
            u2 = U.at(1)
            v2 = V.at(1)
            box2_1 = AABB(q2, q2+u2+v2)
            box2_2 = AABB(q2+u2, q2+v2)
            box2 = enclose([box2_1, box2_2])
            return enclose([box1, box2])

    
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        ray_time = r.time()
        
        n = cross(self.u.at(ray_time),self.v.at(ray_time))
        normal = unit_vector(n)
        w = n / dot(n,n)
        
        
        D = dot(normal, self.Q.at(ray_time))
        denom = dot(normal, r.direction())
        if abs(denom) < 1e-8:
            return False
        
        t = (D - dot(normal, r.origin())) / denom
        if not (ray_tmin <= t <= ray_tmax):
            return False
        intersection = r.at(t)
        
        p = intersection - self.Q.at(ray_time)
        alpha = dot(w, cross(p, self.v.at(ray_time)))
        beta = dot(w, cross(self.u.at(ray_time), p))
        
        if not (alpha > 0 and beta > 0 and alpha+beta <1) :
            return False
        
        rec.t = t
        rec.p = intersection
        rec.material = self.material
        rec.set_face_normal(r, normal)
        rec.u = alpha
        rec.v = beta
        return True