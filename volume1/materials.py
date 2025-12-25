# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 20:07:58 2025

@author: rehma
"""

from abc import ABC, abstractmethod
from ray import ray
from Vec3 import *
from hittable import hit_record
from random import random

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
    def __init__(self,albedo:color, fuzz:float):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1)

    def scatter(self, r: ray, rec: hit_record):
        reflected = reflect(r.direction(), rec.normal)
        reflected = unit_vector(reflected) + (self.fuzz * random_unit_vector())
        scattered = ray(rec.p, reflected)
        flag = (dot(scattered.direction(), rec.normal) > 0)
        return (flag, self.albedo, scattered)

class dielectric(material):
    def __init__(self,refractive_index: float):
        self.refractive_index = refractive_index
    
    def scatter(self, r: ray, rec: hit_record):
        unit_direction = unit_vector(r.direction())
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = (1.0 - cos_theta*cos_theta)**0.5
        attenuation = color(1.0, 1.0, 1.0)
        refractive_index = 1/self.refractive_index if rec.front_face else self.refractive_index
       
        
        if (refractive_index * sin_theta > 1.0) or (reflectance(cos_theta, refractive_index) > random()):
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refractive_index)
        
        scattered = ray(rec.p, direction)
        
        return (True, attenuation, scattered)
