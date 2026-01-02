# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 20:35:35 2025

@author: rehma
"""
from ray import ray
from Vec3 import *
from abc import abstractmethod, ABC

class hit_record:
    def __init__(self):
        self.normal = vec3(0,0,0)
        self.p = point3(0,0,0)
        self.t = 0.0
        self.front_face = None
        self.material = None
        self.u = None
        self.v = None
    
    def copy_from(self, other):
        self.normal = other.normal
        self.p = other.p
        self.t = other.t
        self.front_face = other.front_face
        self.material = other.material
        self.u = other.u
        self.v = other.v

    def set_face_normal(self, r, outward_normal):
        self.front_face = dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if (self.front_face == True) else -outward_normal
        
        
class hittable(ABC):
    @abstractmethod
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float, rec: hit_record):
        pass


