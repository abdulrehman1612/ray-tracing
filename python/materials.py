# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 20:07:58 2025

@author: rehma
"""

from abc import ABC, abstractmethod
from ray import ray
from Vec3 import *
from hittable import hit_record


class material(ABC):
    @abstractmethod
    def scatter(self, r: ray, rec: hit_record, attenuation: color, scattered: ray):
        return (False, None, None)
    
class lambertian(material):
    def __init__(self, albedo:color):
        self.albedo = albedo
    
    def scatter(self, r: ray, rec: hit_record):
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = ray(rec.p,scatter_direction)
        
        return  (True, self.albedo, scattered)

class metal(material):
    def __init__(self,albedo):
        self.albedo = albedo
    
    def scatter(self, r: ray, rec: hit_record):
        reflected = reflect(r.direction(), rec.normal)
        scattered = ray(rec.p, reflected)
        return (True, self.albedo, scattered)