# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 14:59:20 2025

@author: rehma
"""
from hittable import hittable, hit_record
from ray import ray
from Vec3 import dot, point3, vec3

class sphere(hittable):
    def __init__(self, center: point3, radius: float, material):
        self.center = center
        self.radius = radius
        self.material = material
        
    def axis_min(self):
        return vec3(self.center.x() - self.radius, self.center.y() - self.radius, self.center.z() - self.radius)
    
    def axis_max(self):
        return vec3(self.center.x() + self.radius, self.center.y() + self.radius, self.center.z() + self.radius)
    
    
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        oc = self.center - r.origin()
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
        outward_normal = ((rec.p-self.center)/self.radius)
        rec.set_face_normal(r, outward_normal)
        rec.material = self.material
        return True
