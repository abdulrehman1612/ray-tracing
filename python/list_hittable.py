# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 10:46:35 2025

@author: rehma
"""

from hittable import hit_record, hittable
from ray import ray

class list_hittable(hittable):
    def __init__(self):
        self.objects = []
    
    def add(self,obj):
        self.objects.append(obj)
    
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        hit_anything = False
        closest = ray_tmax
        temp = hit_record()

        for obj in self.objects:
            if obj.hit(r, ray_tmin, closest, temp):
                hit_anything = True
                closest = temp.t
                rec.copy_from(temp)

        return hit_anything

