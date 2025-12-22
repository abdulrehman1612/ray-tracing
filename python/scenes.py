# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 21:59:49 2025

@author: rehma
"""

from rtimports import *


def scene():
    world = list_hittable()
    material_ground = lambertian(color(0.8, 0.8, 0.0))
    material_center = lambertian(color(0.1, 0.2, 0.5))
    material_left   = metal(color(0.8, 0.8, 0.8))
    material_right  = metal(color(0.8, 0.6, 0.2))
    
    world.add(sphere(point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(sphere(point3( 0.0,    0.0, -1.2),   0.5, material_center))
    world.add(sphere(point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(sphere(point3( 1.0,    0.0, -1.0),   0.5, material_right))
    
    return world