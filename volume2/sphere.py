# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 14:59:20 2025

@author: rehma
"""
from hittable import hittable, hit_record
from ray import ray
from Vec3 import *
from bvh import AABB, enclose
import numpy as np
from numba import njit

class sphere(hittable):
    def __init__(self, center1: point3, radius: float, material, center2 = None):
        self.center = ray(center1, vec3(0, 0, 0)) if (center2 is None) else ray(center1, center2 - center1)
        self.radius = radius
        self.material = material
        self.aabb = sphere.enclose_aabb(self.center,center2 ,self.radius)
    
    
    
    def enclose_aabb(center, center2,radius):
        
        if center2 is None:
            c = center.origin()
            min_ = vec3(c.x() - radius, c.y() - radius, c.z() - radius)
            max_ = vec3(c.x() + radius, c.y() + radius, c.z() + radius)
            return AABB( min_, max_)
        
        else:
            c1 = center.at(0)
            min_1 = vec3(c1.x() - radius, c1.y() - radius, c1.z() - radius)
            max_1 = vec3(c1.x() + radius, c1.y() + radius, c1.z() + radius)
            
            c2 = center.at(1)
            min_2 = vec3(c2.x() - radius, c2.y() - radius, c2.z() - radius)
            max_2 = vec3(c2.x() + radius, c2.y() + radius, c2.z() + radius)
            
            box1 = AABB( min_1, max_1)
            box2 = AABB( min_2, max_2)
            
            return enclose([box1, box2])
    

        
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    def get_sphere_uv(p, rec):
        rec.u, rec.v = numba_get_sphere_uv(p.as_list())
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        current_center = self.center.at(r.time())
        oc = current_center - r.origin()
        a = r.direction().length_squared()
        h = dot(r.direction(), oc)
        c = oc.length_squared()-self.radius**2
        
        discriminent = h*h-a*c
        
        if discriminent < 0:
            return False
        
        sqrt_d = discriminent**0.5
        root = (h - sqrt_d) / a
        
        
        if root <= ray_tmin or ray_tmax <= root:
            root = (h + sqrt_d) / a
            if root <= ray_tmin or ray_tmax <= root:
                return False

        rec.t = root
        rec.p = r.at(root)
        outward_normal = ((rec.p-current_center)/self.radius)
        rec.set_face_normal(r, outward_normal)
        sphere.get_sphere_uv(outward_normal, rec)
        rec.material = self.material
        return True



@njit
def numba_get_sphere_uv(p):
    pi = np.pi
    theta = np.acos(-p[1])
    phi = np.atan2(-p[2], p[0]) + pi
    u = phi / (2*pi)
    v = theta / pi
    return (u,v)