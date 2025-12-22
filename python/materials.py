# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 20:07:58 2025

@author: rehma
"""

from abc import ABC, abstractmethod
from ray import ray
from Vec3 import vec3, color
from hittable import hit_record


class material(ABC):
    @abstractmethod
    def scatter(self, r: ray, rec: hit_record, attenuation: color, scattered: ray):
        return (False, None, None)
    
class lambertian(material):
    def __init__(self, albedo:color):
        self.albedo = albedo
    
    def scatter(self, r: ray, rec: hit_record):
        scatter_direction = rec.normal + vec3.random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = ray(rec.p,scatter_direction)
        
        return  (True, self.albedo, scattered)