#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 00:20:32 2025

@author: AGU
"""

from hittable import hittable, hit_record
from list_hittable import list_hittable
from bvhnode import *
from aabb import AABB
from ray import ray
import math
import random
from Vec3 import vec3
from bvh import make_BVH

class volume(hittable):
    def __init__(self, obj, C, material):
        self.obj = obj
        self.C = -1/C
        self.mat = material
        
        if isinstance(obj, list_hittable):
            self.bvh = make_BVH(self.obj.objects)
            self.aabb = AABB(self.bvh.aabb().axis_min(),self.bvh.aabb().axis_max())
        else:
            self.bvh = None
            self.aabb = AABB(self.obj.axis_min() , self.obj.axis_max())
    
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        
        rec1 = hit_record()
        rec2 = hit_record()
        
        if self.bvh:
            if not hit_BVH(self.bvh,r, ray_tmin, ray_tmax, rec1):
                return False
            
            
            if not hit_BVH(self.bvh, r, rec1.t+0.0001, float("inf"), rec2):
                return False
            
        else:
            if not self.obj.hit(r, ray_tmin, ray_tmax, rec1):
                return False
            
            
            if not self.obj.hit(r, rec1.t+0.0001, float("inf"), rec2):
                return False
            
        
        if (rec1.t < ray_tmin):
            rec1.t = ray_tmin
            
        if (rec2.t > ray_tmax):
            rec2.t = ray_tmax
        
        if (rec1.t >= rec2.t):
            return False
        
        if (rec1.t < 0):
            rec1.t = 0

        
        ray_length = r.direction().length()
        distance_inside_boundary = (rec2.t - rec1.t) * ray_length
        hit_distance = self.C * math.log(random.random())
        
        if (hit_distance > distance_inside_boundary):
            return False
        
        rec.t = rec1.t + hit_distance / ray_length
        rec.p = r.at(rec.t)

        rec.normal = vec3(1,0,0)
        rec.front_face = True
        rec.material = self.mat
        return True
            
            