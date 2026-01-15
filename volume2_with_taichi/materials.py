#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 01:25:05 2026

@author: AGU
"""

from Vec3 import vec3
from textures import solid_color

class lambertian:
    def __init__(self, albedo_or_texture):
        self.texture = solid_color(albedo_or_texture) if isinstance(albedo_or_texture, vec3) else albedo_or_texture
        self.type = 0

class metal:
    def __init__(self, texture_or_albedo, fuzz):
        self.texture = solid_color(texture_or_albedo) if isinstance(texture_or_albedo, vec3) else texture_or_albedo
        self.fuzz = min(fuzz, 1)
        self.type = 1

class dielectric:
    def __init__(self, refractive_index):
        self.refractive_index = refractive_index
        self.type = 2

class diffuse_light:
    def __init__(self, texture_or_albedo):
        self.texture = solid_color(texture_or_albedo) if isinstance(texture_or_albedo, vec3) else texture_or_albedo
        self.type = 3
        
    
class isotropic:
    def __init__(self, albedo):
        self.texture = solid_color(albedo)
        self.type = 4
