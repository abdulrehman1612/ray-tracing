#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 22:04:43 2025

@author: AGU
"""

from Vec3 import color, point3
from abc import ABC, abstractclassmethod
import math
from rtw_image import rtw_image
from perlin import perlin

class texture(ABC):
    
    @abstractclassmethod
    def value(self, u:float, v: float, p:point3):
        pass


class solid_color(texture):
    def __init__(self, albedo):
        self.albedo = albedo
    
    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float):
        return cls(color(red, green, blue))
    
    def value(self, u:float, v: float, p):
        return self.albedo
    


class checker_texture(texture):
    def __init__(self, scale, even, odd):
        
        self.even = even if isinstance(even, texture) else solid_color(even)
        self.odd = odd if isinstance(odd, texture) else solid_color(odd)
        self.scale = 1/scale
        
        
    
    @classmethod
    def from_colors(cls, scale, c1, c2):
        return cls(scale, solid_color(c1), solid_color(c2))
    
    def value(self, u, v, p):
        x_int = int(math.floor(self.scale*p.x()))
        y_int = int(math.floor(self.scale*p.y()))
        z_int = int(math.floor(self.scale*p.z()))
        
        is_even = (x_int+y_int+z_int)%2 == 0
        
        if is_even:
            return self.even.value(u, v, p)
        else:
            return self.odd.value(u, v, p)


class image_texture(texture):
    def __init__(self, filename):
        self.image = rtw_image(filename)
    
    def value(self, u, v, p):
        if (self.image.height <= 0):
            return color(0,1,1)
        
        u = max(0.0, min(1.0, u))
        v = 1.0 - max(0.0, min(1.0, v))
        
        i = int(u*self.image.width)
        j = int(v*self.image.height)
        pixel = self.image.pixel_data(i, j)
        
        color_scale = 1.0 / 255.0
        return color(pixel[0] * color_scale,pixel[1] * color_scale,pixel[2] * color_scale)
        
            
class noise_texture(texture):
    def __init__(self, scale):
        self.perlin_noise = perlin()
        self.scale = scale
    
    def value(self, u, v, p):
        return color(0.5,0.5,0.5) * (1 + math.sin(self.scale * p.z() + 10 * self.perlin_noise.terbulance(p, 7)))
    
        
    