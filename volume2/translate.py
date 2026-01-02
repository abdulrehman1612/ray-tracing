#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 06:42:54 2025

@author: AGU
"""
from hittable import *
from bvh import *
from aabb import AABB
from list_hittable import list_hittable

class translate(hittable):
    def __init__(self, obj, offset=vec3(0,0,0)):
        self.obj = obj
        self.offset = offset
        
        if isinstance(obj, list_hittable):
            self.bvh = make_BVH(self.obj.objects)
            self.aabb = AABB(self.bvh.aabb().axis_min() + offset,self.bvh.aabb().axis_max() + offset)
        else:
            self.bvh = None
            self.aabb = AABB(self.obj.axis_min() + offset, self.obj.axis_max() + offset)
    
    def axis_min(self):
        return self.aabb.axis_min()
    
    def axis_max(self):
        return self.aabb.axis_max()
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        
        offset_r = ray(r.origin() - self.offset, r.direction(), r.time())
        
        if self.bvh:
            if hit_BVH(self.bvh, offset_r, ray_tmin, ray_tmax, rec):
                rec.p += self.offset
                return True
        else:
            if self.obj.hit(offset_r, ray_tmin, ray_tmax, rec):
                rec.p += self.offset
                return True

        return False