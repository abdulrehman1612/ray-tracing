#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 02:17:26 2026

@author: AGU
"""

from Vec3 import vec3
from rtw_image import rtw_image

class solid_color:
    def __init__(self, albedo):
        self.type = 0
        self.albedo = albedo

class checker_texture:
    def __init__(self, even, odd, scale):
        self.even = solid_color(even) if isinstance(even, vec3) else even
        self.odd = solid_color(odd) if isinstance(odd, vec3) else odd
        self.scale = scale
        self.type = 1

class perlin_noise:
    def __init__(self, scale):
        self.scale = scale
        self.type = 2

class image_texture:
    def __init__(self, image_path):
        self.image = rtw_image(image_path)
        self.type = 3
