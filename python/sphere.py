# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 14:59:20 2025

@author: rehma
"""
from hittable import hittable, hit_record
from ray import ray
from Vec3 import dot, point3, vec3
from bvh import AABB, enclose

class sphere(hittable):
    def __init__(self, center1: point3, radius: float, material, center2 = None):
        self.center = ray(center1, vec3(0, 0, 0)) if (center2 is None) else ray(center1, center2 - center1)
        self.radius = radius
        self.material = material
        self.aabb = sphere.enclose_aabb(self.center,center2 ,self.radius)
    
    
    
    def enclose_aabb(center, center2,radius):
        if center2 is None:
            return AABB(center.origin(),radius*2 , radius*2, radius*2)
        else:
            box1 = AABB(center.at(0), radius*2, radius*2, radius*2)
            box2 = AABB(center.at(1), radius*2, radius*2, radius*2)
            
            return enclose([box1, box2])
    
        

        
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    
    
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
        rec.material = self.material
        return True
